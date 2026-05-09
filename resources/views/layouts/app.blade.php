<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Purchase Module</title>
    
    <!-- This loads Tailwind and your JS (Alpine) -->
    @vite(['resources/css/app.css', 'resources/js/app.js'])
    
    <!-- Required for Livewire to style components -->
    @livewireStyles
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-6xl mx-auto">
        <!-- This $slot is where your PurchaseForm will appear -->
        {{ $slot }}
    </div>

    <!-- Required for Livewire logic to function -->
    @livewireScripts
</body>
</html>