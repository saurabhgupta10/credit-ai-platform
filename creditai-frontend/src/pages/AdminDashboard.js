import React, { useEffect, useState } from "react";
import axios from "axios";

import {
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow
} from "@mui/material";

import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function AdminDashboard() {

  const [data, setData] = useState({
    total_users: 0,
    total_loans: 0,
    approval_rate_percent: 0
  });

  const [loans, setLoans] = useState([]);

  useEffect(() => {

    axios.get("http://localhost:5000/admin-stats")
      .then((res) => {
        setData(res.data);
      })
      .catch((err) => {
        console.log(err);
      });

    axios.get("http://localhost:5000/loans")
      .then((res) => {
        setLoans(res.data);
      })
      .catch((err) => {
        console.log(err);
      });

  }, []);

  const chartData = {
    labels: ["Approved", "Rejected"],
    datasets: [
      {
        data: [
          data.approval_rate_percent,
          100 - data.approval_rate_percent
        ],
        backgroundColor: [
          "#4CAF50",
          "#F44336"
        ]
      }
    ]
  };

  return (

    <Container style={{ marginTop: "40px" }}>

      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>

      {/* Dashboard Cards */}

      <Grid container spacing={3}>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">
                Total Users
              </Typography>
              <Typography variant="h4">
                {data.total_users}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">
                Total Loans
              </Typography>
              <Typography variant="h4">
                {data.total_loans}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">
                Approval Rate
              </Typography>
              <Typography variant="h4">
                {data.approval_rate_percent}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

      </Grid>


      {/* Chart Section */}

      <Card style={{ marginTop: "40px" }}>
        <CardContent>

          <Typography variant="h6" gutterBottom>
            Loan Approval Analytics
          </Typography>

          <div style={{ width: "400px", margin: "auto" }}>
            <Pie data={chartData} />
          </div>

        </CardContent>
      </Card>


      {/* Recent Loan Table */}

      <Card style={{ marginTop: "40px" }}>
        <CardContent>

          <Typography variant="h6" gutterBottom>
            Recent Loan Applications
          </Typography>

          <Table>

            <TableHead>
              <TableRow>
                <TableCell>User</TableCell>
                <TableCell>Income</TableCell>
                <TableCell>Loan Amount</TableCell>
                <TableCell>CIBIL Score</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>

            <TableBody>

              {loans.map((loan, index) => (

                <TableRow key={index}>

                  <TableCell>{loan.user}</TableCell>
                  <TableCell>{loan.income}</TableCell>
                  <TableCell>{loan.loan_amount}</TableCell>
                  <TableCell>{loan.cibil_score}</TableCell>
                  <TableCell>{loan.status}</TableCell>

                </TableRow>

              ))}

            </TableBody>

          </Table>

        </CardContent>
      </Card>

    </Container>

  );

}

export default AdminDashboard;