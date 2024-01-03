import { Component, Input, OnInit } from '@angular/core';
import { ProductCardComponent } from '../product-card/product-card.component';
import { TypeService } from '../../services/type.service';
import { ProductService } from '../../services/product.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-type-card',
  standalone: true,
  templateUrl: './type-card.component.html',
  styleUrl: './type-card.component.css',
  imports: [ProductCardComponent, CommonModule],
  providers: [TypeService, ProductService],
})
export class TypeCardComponent implements OnInit {
  @Input()
  typeId: string = '';
  typeName: string = '';
  typeDescription: string = '';
  products: any[] = [];

  constructor(
    private typeService: TypeService,
    private productService: ProductService
  ) {}

  ngOnInit(): void {
    this.typeService.getType(this.typeId).subscribe((response) => {
      this.typeName = response.name;
      this.typeDescription = response.description;

      this.loadProducts();
    });
  }

  loadProducts() {
    this.productService.getProducts().subscribe((response) => {
      this.products = response.filter(
        (product: { type: string }) => product.type === this.typeId
      );
    });
  }
}
