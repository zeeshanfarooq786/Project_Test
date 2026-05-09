<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Purchase;
use App\Models\PurchaseItem;
use App\Models\Item;
use App\Models\Brand;
use Illuminate\Support\Facades\DB;

class MigrateLegacyData extends Command
{
    // The name of the command you run in terminal
    protected $signature = 'migrate-legacy-data';
    protected $description = 'Migrate legacy purchase data from array to database';

    public function handle()
    {
        // This is the "Legacy Data" usually provided in Part 5
        $legacyData = [
            ['item' => 'Sugar', 'brand' => 'ABC', 'qty' => 5, 'price' => 150],
            ['item' => 'Milk', 'brand' => 'XYZ', 'qty' => 2, 'price' => 250],
            ['item' => 'Sugar', 'brand' => 'ABC', 'qty' => 10, 'price' => 145], // Duplicate combo, different purchase
        ];

        $this->info('Starting migration...');

        DB::transaction(function () use ($legacyData) {
            foreach ($legacyData as $data) {
                // 1. Find or Create Item/Brand IDs
                $item = Item::firstOrCreate(['name' => $data['item']]);
                $brand = Brand::firstOrCreate(['name' => $data['brand']]);

                $alreadyExists = PurchaseItem::where('item_id', $item->id)
                ->where('brand_id', $brand->id)
                ->where('qty', $data['qty'])
                ->where('price', $data['price'])
                ->exists();
                if ($alreadyExists) {
                    $this->line("Skipping {$data['item']} - Already imported.");
                    continue; // Skip to the next item in the loop
                }
                // 3. Only create if it doesn't exist
                $total = $data['qty'] * $data['price'];
                $purchase = Purchase::create(['total' => $total]);

                // 3. Create the Detail PurchaseItem record
                PurchaseItem::create([
                    'purchase_id' => $purchase->id,
                    'item_id' => $item->id,
                    'brand_id' => $brand->id,
                    'qty' => $data['qty'],
                    'price' => $data['price'],
                ]);
                
                $this->info("Imported: {$data['item']} ({$data['brand']})");
            }
        });

        $this->info('Migration completed successfully!');   
    }
}