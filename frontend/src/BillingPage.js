import React, { useState } from "react";
import "./BillingPage.css";
import axios from 'axios';

function BillingPage() {
  const [data, setData] = useState([{ product_Id: "", quantity: "" }]);
  const [customerEmail, setCustomerEmail] = useState("");
  const [error, setError] = useState('');
  const [values, setValues] = useState({
    rupee500: "",
    rupee50: "",
    rupee20: "",
    rupee10: "",
    rupee5: "",
    rupee2: "",
    rupee1: "",
  });

  // To calulate the total Amount
  const calculateTotal = () => {
    const denominations = {
      rupee500: 500,
      rupee50: 50,
      rupee20: 20,
      rupee10: 10,
      rupee5: 5,
      rupee2: 2,
      rupee1: 1,
    };

    return Object.entries(values).reduce((total, [key, value]) => {
      const count = parseFloat(value);
      const denomination = denominations[key];
      return total + (isNaN(count) ? 0 : count * denomination);
    }, 0);
  };

  // Update the note count when it changes
  const handleChange = (event) => {
    const { name, value } = event.target;
    setValues((prevValues) => {
      const newValues = { ...prevValues, [name]: value };
      return newValues;
    });
  };

  // To print the All Json
  const totalJson = async () => {

    const totalAmount = calculateTotal();
    const res = new Object();
    res.customerEmail = customerEmail;
    res.denominations = values;
    res.billSection = data;
    res.totalAmount = totalAmount;
    const result = [
      {
        customerEmail,
        denominations: values,
        billSection: data,
        totalAmount,
      }
    ];

    console.log(res);
    
    const response = await axios.post('http://localhost:8000/api/generatePdf', res
    ).then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data], {type: "application/pdf"}));
      const link = document.createElement('a');
      link.href = url;
      link.download = "Bill.pdf";
      link.click();
    }).catch((error) => {
      console.log("Error")
      setError(error.message);
      console.log(error.message);
    });

    console.log("Success")

  };
  

  //update the Bill Section when it change
  const handleInputChange = (index, column, value) => {
    const newData = [...data];
    newData[index][column] = value;
    setData(newData);
  };

  // Add the row in Bill Section
  const addRow = () => {
    console.log("Data" + data);
    setData((prevData) => [...prevData, { product_Id: "", quantity: "" }]);
  };

  // Remove the row in Bill Section
  const removeRow = (index) => {
    const newData = data.filter((_, i) => i !== index);
    console.log(JSON.stringify(newData, null, 2));
    setData(newData);
  };
  return (
    <div className="container">
      <div className="top-pane">
        <div className="text-style">Billing Page</div>
        <div className="form-group">
          <label htmlFor="customerEmail">Customer Email</label>
          <input
            type="email"
            id="customerEmail"
            name="customerEmail"
            placeholder="Email Id"
            value={customerEmail}
            onChange={(e) => setCustomerEmail(e.target.value)}
          />
        </div>
        <div className="input_button">
          <button variant="contained" onClick={addRow}>
            Add New
          </button>
          <button
            variant="contained"
            onClick={() => removeRow(data.length - 1)}
          >
            Remove
          </button>
        </div>
        <div className="form-group2">
          <label htmlFor="BillSection">Bill section</label>
          <div className="table-container">
            <table className="custom-table">
              <tbody>
                {data.map((row, index) => (
                  <tr key={index}>
                    <td>
                      <input
                        type="text"
                        value={row.product_Id}
                        onChange={(e) =>
                          handleInputChange(index, "product_Id", e.target.value)
                        }
                        placeholder="Product Id"
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        value={row.quantity}
                        onChange={(e) =>
                          handleInputChange(index, "quantity", e.target.value)
                        }
                        placeholder="Quantity"
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="bottom-pane">
        <div className="line"></div>
        <div className="form-group">
          <label htmlFor="Denominations">Denomination</label>
        </div>
        {[
          { id: "rupee500", label: "500" },
          { id: "rupee50", label: "50" },
          { id: "rupee20", label: "20" },
          { id: "rupee10", label: "10" },
          { id: "rupee5", label: "5" },
          { id: "rupee2", label: "2" },
          { id: "rupee1", label: "1" },
        ].map((item) => (
          <div className="form-group3" key={item.id}>
            <div className="labelDiv">
              <label htmlFor={item.id}>{item.label}</label>
            </div>
            <input
              type="number"
              id={item.id}
              name={item.id}
              placeholder="Count"
              value={values[item.id]}
              onChange={handleChange}
            />
          </div>
        ))}
        <div className="form-group">
          <label htmlFor="CashPaidByCustomer">Cash paid by customer</label>
          <input
            type="number"
            id="cashPaidCustomer"
            name="cashPaidCustomer"
            placeholder="Amount"
            value={calculateTotal()}
            readOnly
          />
        </div>
        <div className="input_button">
          <button variant="contained" className="ml-10">
            Cancel
          </button>
          <button variant="contained" onClick={totalJson}>
            Generate Bill
          </button>
        </div>
      </div>
    </div>
  );
}
export default BillingPage;

