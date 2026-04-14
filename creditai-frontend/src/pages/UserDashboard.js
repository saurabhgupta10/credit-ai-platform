import { useEffect, useState } from "react";
import {
  Container,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid
} from "@mui/material";
import API from "../api";

function UserDashboard() {
  const [income, setIncome] = useState("");
  const [loan, setLoan] = useState("");
  const [cibil, setCibil] = useState("");
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(false);

  // ========================
  // FETCH LOANS
  // ========================
  const fetchLoans = async () => {
    try {
      const res = await API.get("/my-loans");
      setLoans(res.data);
    } catch (error) {
      console.error(error);
      alert("Failed to fetch loans ");
    }
  };

  useEffect(() => {
    fetchLoans();
  }, []);

  // ========================
  // APPLY LOAN
  // ========================
  const applyLoan = async () => {
    if (!income || !loan || !cibil) {
      alert("Please fill all fields ");
      return;
    }

    setLoading(true);

    try {
      const res = await API.post("/apply-loan", {
        income: Number(income),
        loan_amount: Number(loan),
        cibil_score: Number(cibil)
      });

      alert("Loan Status: " + res.data.loan_status);

      // Refresh loan list
      fetchLoans();

      // Clear inputs
      setIncome("");
      setLoan("");
      setCibil("");

    } catch (error) {
      console.error(error);

      if (error.response?.status === 401) {
        alert("Please login first ");
      } else {
        alert("Error applying for loan ");
      }
    }

    setLoading(false);
  };

  return (
    <Container style={{ marginTop: "40px" }}>
      <Typography variant="h4" gutterBottom>
        User Dashboard
      </Typography>

      {/* APPLY LOAN CARD */}
      <Card style={{ marginBottom: "30px" }}>
        <CardContent>
          <Typography variant="h6">Apply Loan</Typography>

          <Grid container spacing={2} style={{ marginTop: "10px" }}>
            <Grid item xs={4}>
              <TextField
                label="Income"
                fullWidth
                value={income}
                onChange={(e) => setIncome(e.target.value)}
              />
            </Grid>

            <Grid item xs={4}>
              <TextField
                label="Loan Amount"
                fullWidth
                value={loan}
                onChange={(e) => setLoan(e.target.value)}
              />
            </Grid>

            <Grid item xs={4}>
              <TextField
                label="CIBIL Score"
                fullWidth
                value={cibil}
                onChange={(e) => setCibil(e.target.value)}
              />
            </Grid>
          </Grid>

          <Button
            variant="contained"
            style={{ marginTop: "20px" }}
            onClick={applyLoan}
            disabled={loading}
          >
            {loading ? "Processing..." : "Apply Loan"}
          </Button>
        </CardContent>
      </Card>

      {/* LOAN LIST */}
      <Typography variant="h6">My Loans</Typography>

      {loans.length === 0 ? (
        <Typography>No loans found</Typography>
      ) : (
        loans.map((loan, index) => (
          <Card key={index} style={{ marginTop: "10px" }}>
            <CardContent>
              <Typography>Amount: ₹{loan.loan_amount}</Typography>
              <Typography>Status: {loan.status}</Typography>
              <Typography>EMI: ₹{loan.emi}</Typography>
              <Typography>Tenure: {loan.tenure} months</Typography>
            </CardContent>
          </Card>
        ))
      )}
    </Container>
  );
}

export default UserDashboard;