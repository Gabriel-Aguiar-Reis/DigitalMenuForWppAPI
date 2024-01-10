import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ProductService } from '../../services/product.service';

@Component({
  selector: 'app-searchbar',
  standalone: true,
  imports: [CommonModule],
  providers: [ProductService],
  templateUrl: './searchbar.component.html',
  styleUrl: './searchbar.component.css'
})
export class SearchbarComponent implements OnInit{
  products: any[] = []

  constructor (private productService: ProductService) {}
  ngOnInit(): void {
    this.productService.getProducts().subscribe(
      (response) => {
        this.products = response
      }
    )
  }

}
