<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Purchase History - InventoryPro</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">

    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="text-2xl font-black text-blue-600">InventoryPro</div>
                <div class="flex items-center gap-4">
                    <span class="text-gray-600 text-sm">Hello, {{ auth()->user()->name }}</span>
                    <form action="{{ route('logout') }}" method="POST">
                        @csrf
                        <button type="submit" class="text-sm font-semibold text-red-600 hover:text-red-800">Logout</button>
                    </form>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-10 px-4">
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900">Purchase History</h1>
            <p class="text-gray-500">Viewing all recorded inventory transactions.</p>
        </div>

        <div class="bg-white shadow-xl rounded-2xl overflow-hidden border border-gray-200">
            <table class="w-full text-left border-collapse">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Purchase ID</th>
                        <th class="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Date</th>
                        <th class="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Grand Total</th>
                        <th class="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-center">Status</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                    @forelse($purchases as $purchase)
                        <tr class="hover:bg-gray-50 transition">
                            <td class="p-4 font-mono text-blue-600 font-medium">#PRC-{{ str_pad($purchase->id, 5, '0', STR_PAD_LEFT) }}</td>
                            <td class="p-4 text-gray-600">{{ $purchase->created_at->format('d M, Y h:i A') }}</td>
                            <td class="p-4 text-right font-bold text-gray-900">
                                PKR {{ number_format($purchase->total, 2) }}
                            </td>
                            <td class="p-4 text-center">
                                <span class="bg-green-100 text-green-700 text-xs px-2.5 py-1 rounded-full font-bold uppercase">Completed</span>
                            </td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="4" class="p-10 text-center text-gray-500">
                                No purchases found in the system.
                            </td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
    </main>

</body>
</html>