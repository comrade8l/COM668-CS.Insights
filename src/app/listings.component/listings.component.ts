import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'floats',
  templateUrl: './listings.component.html',
  styleUrls: ['./listings.component.css']
})
export class ListingsComponent {
  float_list: any = [];
  page: number = 1;
  filters = { name: '' };

  constructor(public webService: WebService, private route: ActivatedRoute) {}

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page']);
    }
    this.webService.getFloats(String(this.page)).subscribe((data: any) => {
      this.float_list = data;
    });
  }
}
