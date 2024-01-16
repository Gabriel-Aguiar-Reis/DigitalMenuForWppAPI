import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import {
  Cart,
  sendOrderSuccessfully,
  IAppState,
  getCart,
  setCart,
  setCartSuccessfully,
  sendOrder,
  setTotalOrderPrice,
} from '../store/app.state';
import { map, switchMap, tap, withLatestFrom } from 'rxjs';
import { Store } from '@ngrx/store';

@Injectable({
  providedIn: 'root'
})
export class CartEffectService {
  
  constructor(
    private actions$: Actions,
    private http: HttpClient,
    private store: Store<{ app: IAppState, cart: Cart }>,) {}
  
  private apiUrl = 'http://localhost:8000/api'
    
  getCart = createEffect(
    () => this.actions$.pipe(
      ofType(getCart),
    withLatestFrom(this.store.select('app').pipe(map(app => app.cart))),
    switchMap(([ action, cart ]) => {
      const url = `${this.apiUrl}/cart/view/`
      return this.http.get<any>(url, {withCredentials: true})
      .pipe(
          tap(cart =>  this.store.dispatch(setCart({payload : cart}))),
          map(() => setCartSuccessfully())
        )
      }
    ),
    )
  )

  sendOrder = createEffect(
    () => this.actions$.pipe(
      ofType(sendOrder),
      withLatestFrom(this.store.select('app').pipe(map(app => app.cart))),
      switchMap(([ action, cart ]) => {
        const orderUrl = "https://api.whatsapp.com/send?phone=5512981696818&text=";
        let order = `*NOVO PEDIDO FRESQUINHO*\n`;
  
        for (let product of cart.products) {
          if (product.units > 0) {
            order += `${product.units} x ${product.name}\n`;
  
            for (let ingredient of product.ingredients){
              if (ingredient.qty > 0) {
                order += `  ${ingredient.qty} x ${ingredient.name}\n`;
              }
            }
          }
        }
  
        let totalOrderPrice = this.store.select('app').pipe(map(app => app.totalOrderPrice));
        order += `*Valor Total:* ${totalOrderPrice}`;
  
        const apiEndpoint = orderUrl + encodeURIComponent(order);
        console.log(apiEndpoint)
        return window.location.href = apiEndpoint
  
      }),
      map(() => sendOrderSuccessfully())
    )
  )
}
