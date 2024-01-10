import { Component, Input, OnInit } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { CartService } from '../../services/cart.service';
import { NumberFormatPipe } from '../../pipes/number-format.pipe';

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

  totalUnitsInCart: number = 0
  totalPriceByUnit: number = 0
  
  constructor (private productService: ProductService, private cartService: CartService) {}
  ngOnInit(): void {
    this.productService.getProduct(this.productId).subscribe(
      (response) => {
        this.productPrice = response.price
        this.productName = response.name
        this.productDescription = response.description
      }
    )
  }
  addToCart(): void {
    this.productService.addToCart(this.productId, this.units).subscribe(
      (response) => {

        this.totalUnitsInCart = response.units;

        if (Array.isArray(response.post_discount_price) && response.post_discount_price.length === 2) {
          this.totalPriceByUnit = response.post_discount_price[1];
        } else {
          this.totalPriceByUnit = response.post_discount_price;
        } 
        this.units = 0
        console.log(response);
      },
      (error) => {
        console.error('Erro ao adicionar ao carrinho', error);
      }
    )
  }

  removeFromCart(): void {
    this.productService.removeFromCart(this.productId, this.units).subscribe(
      (response) => {
        this.totalUnitsInCart = response.units

        if (Array.isArray(response.post_discount_price) && response.post_discount_price.length === 2) {
          this.totalPriceByUnit = response.post_discount_price[1];
        } else {
          this.totalPriceByUnit = response.post_discount_price;
        }
        this.units = 0
        console.log(response);
      },
      (error) => {
        console.error('Erro ao remover do carrinho', error);
      }
    )
  }

  addOne(): void {
    this.units += 1;
  }

  removeOne(): void {
    if (this.units > 0){
      this.units -= 1;
    }
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

