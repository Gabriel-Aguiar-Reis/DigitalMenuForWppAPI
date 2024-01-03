import { Component, OnInit } from '@angular/core';
import { MenuTypeComponent } from '../../components/menu-type/menu-type.component';
import { LogoComponent } from '../../components/logo/logo.component';
import { SearchbarComponent } from '../../components/searchbar/searchbar.component';
import { ShoppingCartComponent } from '../../components/shopping-cart/shopping-cart.component';
import { TypeCardComponent } from '../../components/type-card/type-card.component';
import { MenuTypeService } from '../../services/menu-type.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [MenuTypeComponent, ShoppingCartComponent, TypeCardComponent, LogoComponent, SearchbarComponent, CommonModule],
  providers: [MenuTypeService],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit{
  types: any[] = []


  constructor (private menuTypeService: MenuTypeService) {}

  ngOnInit(): void {
    this.menuTypeService.getTypes().subscribe(
      (response) => {
        this.types = response
      }
    );
  }

}
