<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Item;
use App\Models\Brand;
use App\Models\Purchase;
use App\Models\PurchaseItem;
use Illuminate\Support\Facades\DB;

class PurchaseForm extends Component
{
    public $items, $brands;
    public $rows = [];
    public $total = 0;
    public $editingPurchaseId = null; // Track if we are editing

    public function mount()
    {
        $this->items = Item::all();
        $this->brands = Brand::all();
        $this->addRow();
    }

    public function addRow()
    {
        $this->rows[] = ['item_id' => '', 'brand_id' => '', 'qty' => 1, 'price' => 0, 'subtotal' => 0];
    }

    public function removeRow($index)
    {
        unset($this->rows[$index]);
        $this->rows = array_values($this->rows);
    }

    public function save()
    {
        if (auth()->user()->role !== 'admin') return abort(403);

        // 1. Validate the rows (Part 3 Requirement)
        $this->validate([
            'rows.*.item_id' => 'required|integer',
            'rows.*.brand_id' => 'required|integer',
            'rows.*.qty' => 'required|numeric|min:1',
            'rows.*.price' => 'required|numeric|min:0',
        ], [
            'rows.*.item_id.required' => 'Please select an item.',
            'rows.*.brand_id.required' => 'Please select a brand.',
        ]);
        // 2. Prevent Duplicate Combinations (Part 3 Requirement)
        foreach ($this->rows as $index => $row) {
            $exists = \App\Models\PurchaseItem::where('item_id', $row['item_id'])
                        ->where('brand_id', $row['brand_id'])
                        // If we are EDITING, ignore the items already attached to THIS purchase
                        ->when($this->editingPurchaseId, function ($query) {
                            return $query->where('purchase_id', '!=', $this->editingPurchaseId);
                        })
                        ->exists();

            if ($exists) {
                $itemName = \App\Models\Item::find($row['item_id'])->name ?? 'Item';
                $brandName = \App\Models\Brand::find($row['brand_id'])->name ?? 'Brand';
                
                session()->flash('error', "The combination of $itemName and $brandName already exists in the system.");
                return; // Kill the save process
            }
        }

        DB::transaction(function () {
            // If editing, delete old items first
            if ($this->editingPurchaseId) {
                $purchase = Purchase::find($this->editingPurchaseId);
                $purchase->items()->delete();
                $purchase->update(['total' => $this->total]);
            } else {
                $purchase = Purchase::create(['total' => $this->total]);
            }

            foreach ($this->rows as $row) {
                PurchaseItem::create([
                    'purchase_id' => $purchase->id,
                    'item_id' => $row['item_id'],
                    'brand_id' => $row['brand_id'],
                    'qty' => $row['qty'],
                    'price' => $row['price'],
                ]);
            }
        });

        session()->flash('message', $this->editingPurchaseId ? 'Updated!' : 'Saved!');
        $this->resetForm();
    }

    public function edit($id)
    {
        $purchase = Purchase::with('items')->find($id);
        $this->editingPurchaseId = $id;
        $this->total = $purchase->total;
        $this->rows = [];

        foreach ($purchase->items as $item) {
            $this->rows[] = [
                'item_id' => $item->item_id,
                'brand_id' => $item->brand_id,
                'qty' => $item->qty,
                'price' => $item->price,
                'subtotal' => $item->qty * $item->price
            ];
        }
    }

    public function delete($id)
    {
        if (auth()->user()->role !== 'admin') return;
        Purchase::find($id)->delete();
        session()->flash('message', 'Purchase deleted.');
    }

    public function resetForm()
    {
        $this->reset(['rows', 'total', 'editingPurchaseId']);
        $this->addRow();
    }

    public function render()
    {
        return view('livewire.purchase-form', [
            'purchases' => Purchase::with('items.item', 'items.brand')->latest()->get()
        ]);
    }
    public function runMigration()
{
    // Security check
    if (auth()->user()->role !== 'admin') {
        session()->flash('error', 'Unauthorized access.');
        return;
    }

    try {
        // This calls the Artisan command we will create for Part 5
        \Illuminate\Support\Facades\Artisan::call('migrate-legacy-data');
        
        session()->flash('message', 'Legacy migration completed successfully!');
    } catch (\Exception $e) {
        session()->flash('error', 'Migration failed: ' . $e->getMessage());
    }
}
}