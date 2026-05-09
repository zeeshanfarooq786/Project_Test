<?php

use App\Http\Controllers\AuthController;
use App\Livewire\PurchaseForm;
use Illuminate\Support\Facades\Route;

// Guest Routes
Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
Route::post('/login', [AuthController::class, 'login'])->name('login.post');
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// Protected Routes
Route::middleware(['auth'])->group(function () {
    
    // Only Admin can access the Create/Edit page
    Route::get('/purchase/create', PurchaseForm::class)
        ->middleware('role:admin')
        ->name('purchase.create');

    // Users (and Admins) can see the List
    Route::get('/purchases', function() {
        // Fetch all purchases with newest first
        $purchases = \App\Models\Purchase::latest()->get();
        
        return view('purchases.index', compact('purchases'));
    })->name('purchases.index');
});

// Redirect root to login
Route::get('/', function () { return redirect('/login'); });