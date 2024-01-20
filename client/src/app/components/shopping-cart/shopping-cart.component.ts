import {
  IAppState,
  Cart,
  addOneProductToCart,
  removeOneProductFromCart,
  initApp,
  sendOrder,
  addOneIngredientToCart,
  removeOneIngredientFromCart
} from './../../store/app.state';
import { Component, OnInit } from '@angular/core';
import { CartService } from '../../services/cart.service';
import { CommonModule } from '@angular/common';
import { NumberFormatPipe } from '../../pipes/number-format.pipe';
import { Store } from '@ngrx/store';
import { map } from 'rxjs/operators';
import { CartEffectService } from '../../services/cart-effect.service';

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
  isArray(value: any): boolean {return Array.isArray(value);
  }
  constructor (
    private store: Store<{ app: IAppState, cart: Cart }>,
    private cartEffectService: CartEffectService
  ) {}
    
  cart$ = this.store.select('app').pipe(map(app => app.cart));
  products$ = this.store.select('app').pipe(map(app => app.cart.products))
  
  totalOrderPrice$ = this.store.select('app').pipe(map(app => app.totalOrderPrice))

  addOneProductToCart(product: any, products: any) {
    this.store.dispatch(addOneProductToCart({payload : product}))
    this.cartEffectService.calculateTotalOrderPrice(products)
  }
  
  removeOneProductFromCart(product: any, products: any) {
    this.store.dispatch(removeOneProductFromCart({payload : product}))
    this.cartEffectService.calculateTotalOrderPrice(products)
  }

  addOneIngredientToCart(product: any, ingredient: any, products: any) {
    this.store.dispatch(addOneIngredientToCart({payload: {product: product, ingredient: ingredient}}))
    this.cartEffectService.calculateTotalOrderPrice(products)
  }

  removeOneIngredientFromCart(product: any, ingredient: any, products: any) {
    this.store.dispatch(removeOneIngredientFromCart({payload: {product: product, ingredient: ingredient}}))
    this.cartEffectService.calculateTotalOrderPrice(products)
  }

  sendOrder(): void {
    this.store.dispatch(sendOrder())
  }
  ngOnInit(): void {
    this.store.dispatch(initApp())
  }
}
  