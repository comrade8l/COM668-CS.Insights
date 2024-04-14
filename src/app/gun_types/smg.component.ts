import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router'

@Component({
  selector: 'smgs',
  templateUrl: './smg.component.html',
  styleUrls: ['./smg.component.css']
})

export class SMGComponent  {
  smg_list: any = [];
  page: number = 1;
  filters = { name: '',

};

  constructor(public webService: WebService, private route: ActivatedRoute) {}

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page']);
      }
    this.smg_list = this.webService.getSmgSkins(this.page);
    }

    previousPage() {
      if (this.page > 1) {
        this.page = this.page - 1;
        sessionStorage['page'] = this.page;
        this.smg_list = this.webService.getSmgSkins(this.page);
        }
    }

    nextPage() {
      this.page = this.page + 1;
      sessionStorage['page'] = this.page;
      this.smg_list = this.webService.getSmgSkins(this.page);
    }

  }


