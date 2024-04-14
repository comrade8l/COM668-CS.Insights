import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router'

@Component({
  selector: 'heavys',
  templateUrl: './heavy.component.html',
  styleUrls: ['./heavy.component.css']
})

export class HeavyComponent  {
  heavy_list: any = [];
  page: number = 1;
  filters = { name: '',

};

  constructor(public webService: WebService, private route: ActivatedRoute) {}

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page']);
      }
    this.heavy_list = this.webService.getHeavySkins(this.page);
    }

    previousPage() {
      if (this.page > 1) {
        this.page = this.page - 1;
        sessionStorage['page'] = this.page;
        this.heavy_list = this.webService.getHeavySkins(this.page);
        }
    }

    nextPage() {
      this.page = this.page + 1;
      sessionStorage['page'] = this.page;
      this.heavy_list = this.webService.getHeavySkins(this.page);
    }

  }


