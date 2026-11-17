import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, Animal, StockItem } from './core/api.service';
@Component({selector:'app-root', standalone:true, imports:[CommonModule, FormsModule], templateUrl:'./app.component.html'})
export class AppComponent {
  private api = inject(ApiService); email='cuidados@apasfa.org.br'; password=''; loggedIn=false; loading=false; error=''; active='inicio'; animals:Animal[]=[]; stock:StockItem[]=[];
  get lowStock() { return this.stock.filter(i => i.quantity <= i.minimum_quantity); }
  login() { this.loading=true; this.error=''; this.api.login(this.email,this.password).subscribe({next:r=>{this.api.setToken(r.access_token);this.loggedIn=true;this.loadData();},error:()=>{this.error='Não foi possível entrar. Use uma senha definida no ambiente do backend.'},complete:()=>this.loading=false}); }
  loadData() { this.api.getAnimals().subscribe({next:a=>this.animals=a,error:()=>this.error='Não foi possível carregar os prontuários.'}); this.api.getStock().subscribe({next:s=>this.stock=s,error:()=>this.error='Não foi possível carregar o estoque.'}); }
  setActive(tab:string) { this.active=tab; }
}
