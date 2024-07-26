import { NgFor, NgIf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

interface Product {
  id?: number;
  name: string;
  stock: number;
  price: number;
}

@Component({
  selector: 'app-dashboard',
  imports: [FormsModule, NgFor, NgIf,ReactiveFormsModule],
  standalone: true,
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  totalProducts: number = 0;
  outOfStock: number = 0;
  lowStock: number = 0;
  products: Product[] = [];
  newProduct: Product = { name: '', stock: 0, price: 0.00 };
  selectedProduct: Product | null = null;

  constructor(private http: HttpClient) {

    this.fetchDashboardData();
  }


  fetchDashboardData(): void {
    this.http.get<any>('http://127.0.0.1:5000/api/dashboard').subscribe({
      next: (data) => {
        this.totalProducts = data.totalProducts;
        this.outOfStock = data.outOfStock;
        this.lowStock = data.lowStock;
        this.products = data.products;
      },
      error: (error) => {
        console.error('Error fetching dashboard data', error);
      }
    });
  }

  addProduct(): void {
    this.http.post('http://localhost:5000/api/products', this.newProduct).subscribe({
      next: () => {
        this.newProduct = { name: '', stock: 0, price: 0.00 };
        this.fetchDashboardData();
      },
      error: (error) => {
        console.error('Error adding product:', error);
      }
    });
  }

  updateProduct(): void {
    // alert("The product id of selected product is"+this.selectedProduct?.id)
    if (this.selectedProduct && this.selectedProduct.id !== undefined) {
      this.http.put(`http://localhost:5000/api/products/${this.selectedProduct.id}`, this.selectedProduct).subscribe({
        next: () => {
          this.selectedProduct = null;
          this.fetchDashboardData();
        },
        error: (error) => {
          console.error('Error updating product:', error);
        }
      });
    }
  }

  deleteProduct(id: number): void {
    this.http.delete(`http://localhost:5000/api/products/${id}`).subscribe({next: () => {
        this.fetchDashboardData();
      },
      error: (error) => {
        console.error('Error deleting product:', error);
      }
    });
  }

  selectProduct(product: Product): void {
    this.selectedProduct = { ...product };
  }

  clearSelection(): void {
    this.selectedProduct = null;
  }
}