import { Component } from '@angular/core';
// import { ProductService } from '../../product.service';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [],
  templateUrl: './product-card.component.html',
  styleUrl: './product-card.component.css'
})
export class ProductCardComponent {
  // productId: string = '7426ad0c-08b7-4cb0-ad43-81461fcda516';
  unitsToShop: number = 0;
  totalUnitsInCart: number = 0;
  
  // constructor (private productService: ProductService) {}
  addToCart(): void {
    this.totalUnitsInCart += this.unitsToShop
  }
  removeFromCart(): void {
    this.totalUnitsInCart = 0;
    this.unitsToShop = 0;
  }
  // addToCart(): void {
  //   this.productService.updateUnitsPurchased(this.productId, this.unitsToAdd).subscribe(
  //     (response) => {
  //       this.totalUnitsInCart = response.products[this.productId];
  //       console.log(response);
  //     },
  //     (error) => {
  //       console.error('Erro ao adicionar ao carrinho', error);
  //     }
  //   );
  // }

  addOne(): void {
    this.unitsToShop += 1;
  }

  removeOne(): void {
    if (this.unitsToShop > 0){
      this.unitsToShop -= 1;
    }
  }
}

