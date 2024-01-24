import { Component, Input, OnInit } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { CartService } from '../../services/cart.service';
import { NumberFormatPipe } from '../../pipes/number-format.pipe';
import { Store } from '@ngrx/store';
import { addOneProductToCart, Cart, IAppState } from '../../store/app.state';
import { map } from 'rxjs';
import { ShoppingCartComponent } from '../shopping-cart/shopping-cart.component';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [NumberFormatPipe, ShoppingCartComponent],
  providers: [ProductService, CartService],
  templateUrl: './product-card.component.html',
  styleUrl: './product-card.component.css'
})
export class ProductCardComponent implements OnInit{
  constructor (
    private productService: ProductService,
    private store: Store<{ app: IAppState, cart: Cart }>,
    ) {}
  @Input()
  productId: string = ''
  productPrice: number = 0
  productName: string = ''
  productDescription: string = ''
  product: any = null
  
  cart$ = this.store.select('app').pipe(map(app => app.cart));
  products$ = this.store.select('app').pipe(map(app => app.cart.products));

  ngOnInit(): void {
    this.productService.getProduct(this.productId).subscribe(
      (response) => {
        this.productPrice = response.price
        this.productName = response.name
        this.productDescription = response.description
        this.product = response
      }
    )
    }

  addOne(product: any): void {
    this.store.dispatch(addOneProductToCart({payload: product}))
  }
}

