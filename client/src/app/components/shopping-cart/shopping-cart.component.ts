import { Cart } from './../../interfaces/cart';
import { Component, OnInit } from '@angular/core';
import { CartService } from '../../services/cart.service';
import { CommonModule } from '@angular/common';
import { NumberFormatPipe } from '../../pipes/number-format.pipe';

@Component({
  selector: 'app-shopping-cart',
  standalone: true,
  imports: [CommonModule, NumberFormatPipe],
  providers: [CartService],
  templateUrl: './shopping-cart.component.html',
  styleUrl: './shopping-cart.component.css'
})


export class ShoppingCartComponent implements OnInit{
  cart: Cart = {"products": []}
  constructor (private cartService: CartService) {}
  ngOnInit(): void {
    this.cartService.getCart().subscribe(
      (response) => {
        for (const product of response.products) {
          if (product.post_discount_price.length > 1) {
            product.post_discount_price = product.post_discount_price[product.post_discount_price.length - 1];
          }
        }
        console.log(response)
        this.cart = response
      }
    )
  }
}
