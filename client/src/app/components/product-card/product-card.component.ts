import { Component, Input, OnInit } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { CartService } from '../../services/cart.service';
import { NumberFormatPipe } from '../../pipes/number-format.pipe';
import { Store } from '@ngrx/store';
import { addOneToCart, Cart, IAppState, setTotalOrderPrice } from '../../store/app.state';
import { map } from 'rxjs';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [NumberFormatPipe],
  providers: [ProductService, CartService],
  templateUrl: './product-card.component.html',
  styleUrl: './product-card.component.css'
})
export class ProductCardComponent implements OnInit{
  @Input()
  productId: string = ''
  productPrice: number = 0
  units: number = 0
  productName: string = ''
  productDescription: string = ''
  product: any = null

  totalUnitsInCart: number = 0
  totalPriceByUnit: number = 0
  
  constructor (
    private productService: ProductService,
    private cartService: CartService,
    private store: Store<{ app: IAppState, cart: Cart }>
    ) {}

  cart$ = this.store.select('app').pipe(map(app => app.cart));
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

  addOne(product: any, cart: any): void {
    this.store.dispatch(addOneToCart({payload: product}))
    this.store.dispatch(setTotalOrderPrice({payload : cart}))
  }

  cartClear(): void {
    this.cartService.cartClear().subscribe(
      (response) => {
        this.totalPriceByUnit = 0
        this.totalUnitsInCart = 0
        this.units = 0
        console.log(response)
      } 
    )
  }
}

