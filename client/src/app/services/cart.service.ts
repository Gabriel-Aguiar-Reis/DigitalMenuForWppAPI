import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Cart } from '../store/app.state';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getCart(): Observable<any> {
    const url = `${this.apiUrl}/cart/view/`;
    return this.http.get<Cart>(url, {withCredentials: true})
  }
  
  cartClear(): Observable<any> {
    const url = `${this.apiUrl}/cart/clear/`;
    return this.http.delete<any>(url, {withCredentials: true})
  }
}
