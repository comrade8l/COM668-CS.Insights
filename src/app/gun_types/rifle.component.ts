import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router'

@Component({
  selector: 'rifles',
  templateUrl: './rifle.component.html',
  styleUrls: ['./rifle.component.css']
})

export class rifleComponent  {
  rifle_list: any = [];
  page: number = 1;
  filters = { name: '',

};

  constructor(public webService: WebService, private route: ActivatedRoute) {}

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page']);
      }
    this.rifle_list = this.webService.getRifleSkins(this.page);
    }

    previousPage() {
      if (this.page > 1) {
        this.page = this.page - 1;
        sessionStorage['page'] = this.page;
        this.rifle_list = this.webService.getRifleSkins(this.page);
        }
    }

    nextPage() {
      this.page = this.page + 1;
      sessionStorage['page'] = this.page;
      this.rifle_list = this.webService.getRifleSkins(this.page);
    }

  }


