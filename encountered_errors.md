
# Encountered Errors and Solutions

## Secret Scope Creation Without Key Vault

**Problem:** Unable to create a secret scope without using Azure Key Vault.

**Solution:** Implemented environment variables as an alternative to manage secrets.

---

## Git History Merge Conflict

**Problem:** Merge conflict occurred when modifying git history in Databricks.

**Solution:** Removed the connection and re-established it.

---

## CSV Column Type Inference Issue

**Problem:** When reading CSV with `inferSchema=True`, the `stomp` column was inferred as `DOUBLE` (0.0/1.0) instead of `BOOLEAN`, causing a type mismatch error when comparing it to `True`.

**Solution:** Changed the comparison from `col("stomp") == True` to `col("stomp") == 1.0` to ensure both sides use numeric types.


---

## Microsoft.Databricks Resource Provider Not Registered

**Problem:** Resource provider `Microsoft.Databricks` not registered with insufficient permissions.

**Solution:** 
1. Have a Subscription Owner register: Azure Portal → **Subscriptions** → **Resource providers** → **Microsoft.Databricks** → **Register**
2. Assign appropriate IAM permissions in subscription settings
 


---

## Storage Account Region Issue

**Problem:** Initially created the storage account in Poland, but the Databricks service was not available in that region.

**Solution:** Created a new storage account named `dota2lakehousenew` in the EU West region.