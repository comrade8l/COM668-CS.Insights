import { Component, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { InventoryService } from '../inventory.service'; // Update the path as per your file structure

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
calculatePercentageIncrease(arg0: any,arg1: any) {
throw new Error('Method not implemented.');
}
  featuredSkins: any[] = [];

  constructor(public authService: AuthService, private inventoryService: InventoryService) {}

  ngOnInit() {
    this.inventoryService.getFeaturedSkins().subscribe(data => {
      this.featuredSkins = data;
    }, error => console.error('Error fetching skins:', error));
  }
}


export class YourComponent {
  calculatePercentageIncrease(currentPrice: number, previousPrice: number): string {
    const increase = ((currentPrice - previousPrice) / previousPrice) * 100;
    return `${increase.toFixed(1)}%`;
  }
}
