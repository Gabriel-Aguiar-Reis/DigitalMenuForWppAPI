import { Component } from '@angular/core';
import { MenuTypeService } from '../../services/menu-type.service';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-menu-type',
    standalone: true,
    templateUrl: './menu-type.component.html',
    styleUrl: './menu-type.component.css',
    imports: [CommonModule],
    providers: [MenuTypeService],
})
export class MenuTypeComponent {
    types: string[] = [];
  
    constructor(private menuTypeService: MenuTypeService) {}
  
    ngOnInit(): void {
      this.menuTypeService.getTypes().subscribe(
        (response: any) => {
          for (const type in response) {
            if (response.hasOwnProperty(type)) {
              this.types.push(response[type].name);
            }
          }
        }
      )
    }
  }