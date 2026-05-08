<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PurchaseItem extends Model
{
    public $timestamps = false;
    protected $fillable = ['purchase_id', 'item_id', 'brand_id', 'qty', 'price'];

    public function item() {
        return $this->belongsTo(Item::class);
    }

    public function brand() {
        return $this->belongsTo(Brand::class);
    }
}
