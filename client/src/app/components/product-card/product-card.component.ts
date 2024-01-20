import { Component, Input, OnInit } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { CartService } from '../../services/cart.service';
import { NumberFormatPipe } from '../../pipes/number-format.pipe';
import { Store } from '@ngrx/store';
import { addOneProductToCart, Cart, IAppState } from '../../store/app.state';
import { map } from 'rxjs';
import { CartEffectService } from '../../services/cart-effect.service';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [NumberFormatPipe],
  providers: [ProductService, CartService],
  templateUrl: './product-card.component.html',
  styleUrl: './product-card.component.css'
})
export class ProductCardComponent implements OnInit{
  constructor (
    private productService: ProductService,
    private cartService: CartService,
    private store: Store<{ app: IAppState, cart: Cart }>,
    private cartEffectService: CartEffectService
    ) {}
  @Input()
  productId: string = ''
  productPrice: number = 0
  units: number = 0
  productName: string = ''
  productDescription: string = ''
  product: any = null

  totalUnitsInCart: number = 0
  totalPriceByUnit: number = 0
  
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

  addOne(product: any, products: any): void {
    this.store.dispatch(addOneProductToCart({payload: product}))
    this.cartEffectService.calculateTotalOrderPrice(products)
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

