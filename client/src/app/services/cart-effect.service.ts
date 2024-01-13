import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Cart, IAppState, getCart, setCart, setCartSuccessfully } from '../store/app.state';
import { of, map, switchMap, tap, withLatestFrom } from 'rxjs';
import { Store } from '@ngrx/store';

@Injectable({
  providedIn: 'root'
})
export class CartEffectService {
  
  constructor( private actions$: Actions, private http: HttpClient, private store: Store<{ app: IAppState, cart: Cart }>,) {}
  
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
}
