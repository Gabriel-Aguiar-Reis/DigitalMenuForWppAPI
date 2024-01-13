import { IAppState, Cart, addOneToCart, removeOneFromCart, getCart } from './../../store/app.state';
import { Component, OnInit } from '@angular/core';
import { CartService } from '../../services/cart.service';
import { CommonModule } from '@angular/common';
import { NumberFormatPipe } from '../../pipes/number-format.pipe';
import { Store } from '@ngrx/store';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-shopping-cart',
  standalone: true,
  imports: [CommonModule, NumberFormatPipe],
  providers: [CartService],
  templateUrl: './shopping-cart.component.html',
  styleUrl: './shopping-cart.component.css'
})


export class ShoppingCartComponent implements OnInit{
  
  constructor (
    private store: Store<{ app: IAppState, cart: Cart }>,
  ) {}
    
  cart$ = this.store.select('app').pipe(map(app => app.cart));
  products$ = this.store.select('app').pipe(map(app => app.cart.products))

  // addOneToCart() {
  //   this.store.dispatch(addOneToCart())
  // }

  // removeOneFromCart() {
  //   this.store.dispatch(removeOneFromCart())
  // }

  ngOnInit(): void {
    
    this.store.dispatch(getCart())

  }
}
  