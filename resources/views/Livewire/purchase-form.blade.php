<div class="bg-gray-50 min-h-screen">
    <!-- Admin Navbar -->
    <nav class="bg-white shadow-sm border-b mb-8">
        <div class="max-w-7xl mx-auto px-4 h-16 flex justify-between items-center">
            <div class="text-xl font-bold text-blue-600">InventoryPro <span class="text-gray-400">| Admin</span></div>
            <div class="flex items-center gap-4">
                <button wire:click="runMigration" class="bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold px-3 py-2 rounded shadow-sm transition">
                    Run Legacy Migration
                </button>
                <span class="text-sm text-gray-500">{{ auth()->user()->name }}</span>
                <form action="{{ route('logout') }}" method="POST"> @csrf
                    <button type="submit" class="text-red-500 text-sm font-bold">Logout</button>
                </form>
            </div>
        </div>
    </nav>

    <div class="max-w-6xl mx-auto px-4" x-data="{ 
        rows: @entangle('rows'),
        calculate() {
            let grandTotal = 0;
            this.rows.forEach(row => {
                row.subtotal = (row.qty || 0) * (row.price || 0);
                grandTotal += row.subtotal;
            });
            $wire.total = grandTotal;
        }
    }">
    {{-- message --}}
        @if (session()->has('message'))
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
                {{ session('message') }}
            </div>
        @endif

        @if (session()->has('error'))
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                {{ session('error') }}
            </div>
        @endif
        <!-- Form Section -->
        <div class="bg-white p-6 rounded-xl shadow-sm border mb-8">
            <h2 class="text-lg font-bold mb-4">{{ $editingPurchaseId ? 'Edit Purchase #' . $editingPurchaseId : 'New Purchase Entry' }}</h2>
            
            <table class="w-full mb-4">
               <template x-for="(row, index) in rows" :key="index">
                <tr class="border-b">
                    <td class="p-2">
                        <select x-model="row.item_id" class="w-full border-gray-300 rounded">
                            <option value="">Select Item</option>
                            @foreach($items as $item) <option value="{{ $item->id }}">{{ $item->name }}</option> @endforeach
                        </select>
                        @error('rows.*.item_id') <span class="text-red-500 text-xs">Required</span> @enderror
                    </td>
                    
                    <td class="p-2">
                        <select x-model="row.brand_id" class="w-full border-gray-300 rounded">
                            <option value="">Select Brand</option>
                            @foreach($brands as $brand) <option value="{{ $brand->id }}">{{ $brand->name }}</option> @endforeach
                        </select>
                        @error('rows.*.brand_id') <span class="text-red-500 text-xs">Required</span> @enderror
                    </td>
                        <td class="p-2"><input type="number" x-model="row.qty" @input="calculate()" class="w-20 border-gray-300 rounded"></td>
                        <td class="p-2"><input type="number" x-model="row.price" @input="calculate()" class="w-24 border-gray-300 rounded"></td>
                        <td class="p-2 text-right font-bold" x-text="row.subtotal"></td>
                        <td class="p-2 text-center">
                            <button @click="rows.splice(index, 1); calculate()" class="text-red-500">×</button>
                        </td>
                    </tr>
                </template>
            </table>

            <div class="flex justify-between items-center">
                <button @click="$wire.addRow()" class="bg-gray-100 px-4 py-2 rounded text-sm">+ Add Row</button>
                <div class="text-right">
                    <div class="text-2xl font-bold text-blue-600">Total: PKR <span x-text="$wire.total"></span></div>
                    <button wire:click="save" class="mt-2 bg-blue-600 text-white px-8 py-2 rounded font-bold shadow-lg">
                        {{ $editingPurchaseId ? 'Update Record' : 'Save Record' }}
                    </button>
                    @if($editingPurchaseId)
                        <button wire:click="resetForm()" class="mt-2 bg-gray-500 text-white px-4 py-2 rounded ml-2">Cancel</button>
                    @endif
                </div>
            </div>
        </div>

        <!-- History Table Section -->
        <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
            <div class="p-4 border-b bg-gray-50 font-bold">Recent Purchases</div>
            <table class="w-full text-left">
                <thead class="bg-gray-50 text-xs text-gray-500 uppercase">
                    <tr>
                        <th class="p-4">ID</th>
                        <th class="p-4">Items</th>
                        <th class="p-4 text-right">Total</th>
                        <th class="p-4 text-center">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y">
                    @foreach($purchases as $p)
                    <tr class="hover:bg-gray-50">
                        <td class="p-4 font-bold">#{{ $p->id }}</td>
                        <td class="p-4 text-sm">
                            @foreach($p->items as $pi)
                                <span class="inline-block bg-gray-100 rounded px-2 py-1 mb-1">{{ $pi->item->name }} ({{ $pi->qty }})</span>
                            @endforeach
                        </td>
                        <td class="p-4 text-right font-bold text-blue-600">PKR {{ number_format($p->total) }}</td>
                        <td class="p-4 text-center">
                            <button wire:click="edit({{ $p->id }})" class="text-blue-500 hover:underline mr-3">Edit</button>
                            <button onclick="confirm('Delete?') || event.stopImmediatePropagation()" wire:click="delete({{ $p->id }})" class="text-red-500 hover:underline">Delete</button>
                        </td>
                    </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
    </div>
</div>