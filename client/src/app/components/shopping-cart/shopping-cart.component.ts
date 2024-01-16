import { IAppState, Cart, addOneToCart, removeOneFromCart, getCart, sendOrder, setTotalOrderPrice } from './../../store/app.state';
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
  Number(string: string) {return parseFloat(string)}
  constructor (
    private store: Store<{ app: IAppState, cart: Cart }>,
  ) {}
    
  cart$ = this.store.select('app').pipe(map(app => app.cart));
  products$ = this.store.select('app').pipe(map(app => app.cart.products))
  totalOrderPrice$ = this.store.select('app').pipe(map(app => app.totalOrderPrice))

  addOneToCart(product: any, products: any) {
    this.store.dispatch(addOneToCart({payload : product}))
    this.store.dispatch(setTotalOrderPrice({payload : products}))
  }

  removeOneFromCart(product: any) {
    this.store.dispatch(removeOneFromCart({payload : product}))
  }

  sendOrder(): void {
    this.store.dispatch(sendOrder())
  }
  ngOnInit(): void {
    
    this.store.dispatch(getCart())

  }
}
  