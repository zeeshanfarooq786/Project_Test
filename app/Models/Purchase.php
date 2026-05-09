<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Purchase extends Model
{
    protected $fillable = ['total'];

    public function items() {
        return $this->hasMany(PurchaseItem::class);
    }
}
