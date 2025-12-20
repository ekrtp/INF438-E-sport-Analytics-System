# Databricks Setup Guide

## 🔐 Setting Up Secrets in Databricks

### Option 1: Using Databricks UI (Simplest)

1. **Navigate to Databricks Workspace**
   - Go to your Azure Databricks workspace URL

2. **Access Settings**
   - Click your username (top right)
   - Select **Settings** → **Developer** → **Access tokens**

3. **Create Secret Scope** (via CLI - see below)
   - Databricks UI doesn't have direct secret scope creation
   - You need to use Databricks CLI or Azure Key Vault

### Option 2: Using Databricks CLI (Recommended)

```bash
# 1. Install Databricks CLI
pip install databricks-cli

# 2. Configure authentication
databricks configure --token
# You'll be prompted for:
# - Databricks Host: https://<your-workspace>.azuredatabricks.net
# - Token: Generate from User Settings → Developer → Access Tokens

# 3. Create secret scope
databricks secrets create-scope --scope azure-storage

# 4. Add your storage key as a secret
databricks secrets put-secret azure-storage storage-account-key --string-value "7/6FSxxxxxxxxxxxxxxxxx"

# 5. Verify secrets
databricks secrets list-scopes
databricks secrets list-secrets azure-storage
```

### Option 3: Using Azure Key Vault (Most Secure for Production)

1. **Create Azure Key Vault**
   ```bash
   az keyvault create \
     --name dota2-secrets \
     --resource-group your-resource-group \
     --location eastus
   ```

2. **Add Secret to Key Vault**
   ```bash
   az keyvault secret set \
     --vault-name dota2-secrets \
     --name storage-account-key \
     --value "7/6FSxxxxxxxxxxxxxxxxx"
   ```

3. **Link to Databricks**
   ```bash
   databricks secrets create-scope \
     --scope azure-storage \
     --scope-backend-type AZURE_KEYVAULT \
     --resource-id "/subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.KeyVault/vaults/dota2-secrets" \
     --dns-name "https://dota2-secrets.vault.azure.net/"
   ```

## 🔧 Setting Cluster Environment Variables (Optional)

For non-sensitive configuration, you can set environment variables at the cluster level:

1. **Navigate to Compute** in Databricks
2. **Select your cluster** → **Edit**
3. **Advanced Options** → **Spark** → **Environment Variables**
4. Add:
   ```
   spark.azure.storage.account=dota2lakehouse
   spark.azure.container=data
   ```

## 📂 How the Notebooks Work Now

### Local Development (.env file)
```bash
# Your .env file (already exists locally)
AZURE_STORAGE_ACCOUNT_NAME=dota2lakehouse
AZURE_STORAGE_ACCOUNT_KEY=7/6FSxxxxxxxxxxxxxxxxx
AZURE_CONTAINER_NAME=data
```

### Databricks (Secrets + Config)
```python
# Automatically detected by notebooks
storage_account_key = dbutils.secrets.get(scope="azure-storage", key="storage-account-key")
storage_account = "dota2lakehouse"  # Hardcoded fallback
container = "data"  # Hardcoded fallback
```

## 🚀 Running the Notebooks in Databricks

### Step 1: Upload Notebooks
1. Go to **Workspace** in Databricks
2. Right-click → **Import**
3. Upload all `.ipynb` files from `scripts/` folder

### Step 2: Create/Attach Cluster
1. **Compute** → **Create Cluster**
2. **Databricks Runtime**: 13.3 LTS or higher (includes Delta Lake)
3. **Node Type**: Choose based on your workload
4. **Auto-termination**: 30 minutes (to save costs)

### Step 3: Run in Order
1. **setup_connection.ipynb** - Test connection
2. **bronze_to_silver.ipynb** - Data cleaning
3. **silver_to_gold.ipynb** - Aggregations
4. **sql_analysis.ipynb** - Analytics

## 🔍 Troubleshooting

### Error: "Scope 'azure-storage' does not exist"
```bash
# Create the scope
databricks secrets create-scope --scope azure-storage
databricks secrets put-secret azure-storage storage-account-key
```

### Error: "Storage account key not found"
```python
# Check if secret exists
dbutils.secrets.list("azure-storage")

# Test secret retrieval
print(dbutils.secrets.get(scope="azure-storage", key="storage-account-key")[:5] + "...")
```

### Error: "This operation requires ADLS Gen2 account"
- Ensure your storage account has **Hierarchical namespace enabled**
- Check Azure Portal → Storage Account → Properties

### Error: "401 Unauthorized"
- Verify your storage key is correct
- Check if key has been rotated in Azure

## 📊 Local vs Databricks Comparison

| Feature | Local (.env) | Databricks (Secrets) |
|---------|-------------|----------------------|
| Credentials | .env file | Databricks Secrets |
| Path Variables | os.getenv() | dbutils.secrets.get() |
| Spark Session | Pre-configured | Pre-configured |
| File System | ABFS URLs | ABFS URLs |
| Detection | IS_DATABRICKS = False | IS_DATABRICKS = True |

## ✅ Verification Checklist

- [ ] Databricks CLI installed and configured
- [ ] Secret scope `azure-storage` created
- [ ] Secret `storage-account-key` added
- [ ] Cluster created with runtime 13.3+
- [ ] Notebooks uploaded to workspace
- [ ] `setup_connection.ipynb` runs successfully
- [ ] Can see files in Bronze layer

## 🔗 Useful Commands

```bash
# List all secret scopes
databricks secrets list-scopes

# List secrets in a scope (values are redacted)
databricks secrets list-secrets azure-storage

# Delete a secret
databricks secrets delete-secret azure-storage storage-account-key

# Delete a scope
databricks secrets delete-scope azure-storage

# Check cluster status
databricks clusters list
```

## 🎯 Next Steps

After setup:
1. Run `setup_connection.ipynb` to verify everything works
2. Check Bronze layer files are accessible
3. Run the data pipeline notebooks in sequence
4. Use `sql_analysis.ipynb` for queries

---

**Need Help?** Check Databricks documentation:
- [Secrets Management](https://docs.databricks.com/security/secrets/index.html)
- [Azure Data Lake Storage Gen2](https://docs.microsoft.com/en-us/azure/databricks/data/data-sources/azure/adls-gen2/)
