
# DRL Management System

A comprehensive command-line tool for managing Drools Rule Language (DRL) files with AI assistance, featuring intelligent context management and rate limiting for the Groq API.

## Features

- **Repository Scanning**: Automatically scans for Java models, DRL files, and GDST files
- **AI-Powered Rule Generation**: Generate new DRL rules using Groq's LLM
- **Rule Modification**: Modify existing DRL rules with precise requirements
- **Context-Aware**: Maintains full repository context (Java models, existing rules, GDST tables)
- **Rate Limiting**: Strict 6000 tokens/minute enforcement for Groq API
- **Chunk Optimization**: Intelligent context splitting for large repositories
- **Interactive CLI**: User-friendly command-line interface
- **File Management**: View, edit, and manage DRL files

## Token Management & Chunking Optimization

The system implements several advanced features to work within Groq's limits:

- **Token Bucket Algorithm**: Strict 6000 tokens/minute rate limiting
- **Smart Chunking**: 
  - Splits large context into optimally sized chunks (~4000 tokens)
  - Preserves logical file structure when splitting
  - Progress tracking during context loading
- **Token Estimation**: 
  - Uses 1 token ≈ 4 characters approximation
  - Includes buffers for prompt overhead
- **Efficient Loading**: 
  - Parallel processing where possible
  - Visual progress indicators

## Quick Start

### Installation

1. Ensure Python 3.8+ is installed
2. Install required packages:
   ```bash
   pip install groq python-dotenv
   ```
3. Set your Groq API key:
   ```bash
   drl config set-api-key YOUR_API_KEY
   ```

### Basic Usage

```bash
# Scan a repository
drl scan /path/to/your/project

# List all DRL files
drl list drl

# Generate a new rule
drl generate --output new_rule.drl

# Modify an existing rule
drl modify existing_rule.drl

# Interactive mode
drl --interactive
```

## Command Reference

### Main Commands

| Command       | Parameters                      | Description                                  |
|---------------|---------------------------------|----------------------------------------------|
| `scan`        | `[path]`                       | Scan repository for DRL-related files        |
| `list`        | `[all\|java\|drl\|gdst]`       | List found files of specified type           |
| `view`        | `<file_path>`                  | View content of a specific file              |
| `edit`        | `[file_path]`                  | Edit file (creates new if not specified)     |
| `generate`    | `[--output FILE]` `[--requirements TEXT]` | Generate new DRL rule            |
| `modify`      | `[file_path]` `[--requirements TEXT]` | Modify existing DRL rule          |
| `context`     | `[--limit CHARS]`              | Show repository context                      |
| `config`      | `[action]` `[value]`           | Configure application settings               |

### Configuration Actions

| Action           | Description                          |
|------------------|--------------------------------------|
| `set-api-key`    | Set Groq API key                     |
| `set-repository` | Set default repository path          |
| `set-editor`     | Set preferred text editor            |
| `show`           | Show current configuration           |

## Examples

### 1. Full Workflow Example

```bash
# Set your API key
drl config set-api-key your_groq_api_key_here

# Scan a project
drl scan ~/projects/rules-engine

# List all DRL files
drl list drl

# Generate a new discount rule
drl generate --output discount_rules.drl

# Modify an existing validation rule
drl modify validation_rules.drl
```

### 2. Interactive Mode Example

```bash
C:\Users\ganes\Downloads\tkinter-drl-system>python drl_management_system.py --interactive
=== DRL Management System - Interactive Mode ===
Type 'help' for available commands or 'quit' to exit

drl> scan
Scanning repository: C:\Users\ganes\Downloads\tkinter-drl-system
Found: 6 Java model files, 6 DRL files, 2 GDST files
Repository scan completed successfully!
Loading context into LLM memory...
Sending context chunk 1/2 (approx. 4264 tokens)...
Sending context chunk 2/2 (approx. 3742 tokens)...
Context loading complete!

drl> modify

Select a DRL file to modify:

=== DRL Rule Files ===
 1. new_rule_20250703_153606.drl (C:\Users\ganes\Downloads\tkinter-drl-system\new_rule_20250703_153606.drl) - 166 bytes
 2. new_rule_20250703_153613.drl (C:\Users\ganes\Downloads\tkinter-drl-system\new_rule_20250703_153613.drl) - 166 bytes
 3. new_rule_20250709_113356.drl (C:\Users\ganes\Downloads\tkinter-drl-system\new_rule_20250709_113356.drl) - 166 bytes
 4. customer-loyalty.drl (C:\Users\ganes\Downloads\tkinter-drl-system\example-springboot-project\src\main\resources\rules\customer-loyalty.drl) - 2835 bytes
 5. order-discounts.drl (C:\Users\ganes\Downloads\tkinter-drl-system\example-springboot-project\src\main\resources\rules\order-discounts.drl) - 4276 bytes
 6. risk-assessment.drl (C:\Users\ganes\Downloads\tkinter-drl-system\example-springboot-project\src\main\resources\rules\risk-assessment.drl) - 2588 bytes

Enter file number to modify: 4

Current content of C:\Users\ganes\Downloads\tkinter-drl-system\example-springboot-project\src\main\resources\rules\customer-loyalty.drl:
==================================================
package com.example.drools.rules;

import com.example.drools.model.Customer;
import com.example.drools.model.CustomerType;
import com.example.drools.model.Order;

// Customer loyalty and tier upgrade rules

rule "Upgrade to Premium Customer"
    when
        $customer : Customer(
            customerType == CustomerType.REGULAR,
            totalSpent > 5000.0,
            loyaltyPoints > 1000
        )
    then
        $customer.setCustomerType(CustomerType.PREMIUM);
        $customer.addLoyaltyPoints(500); // Bonus points for upgrade
        System.out.println("Customer " + $customer.getFullName() + " upgraded to Premium");
end

rule "Upgrade to VIP Customer"
    when
        $customer : Customer(
            customerType == CustomerType.PREMIUM,
            totalSpent > 15000.0,
            loyaltyPoints > 5000
        )
    then
        $customer.setCustomerType(CustomerType.VIP);
        $customer.addLoyaltyPoints(1000); // Bonus points for VIP upgrade
        System.out.println("Customer " + $customer.getFullName() + " upgraded to VIP");
end

rule "Award Loyalty Points for Order"
    when
        $order : Order(status == com.example.drools.model.OrderStatus.DELIVERED)
        $customer : Customer(id == $order.customerId)
    then
        int points = (int) ($order.getTotalAmount() / 10); // 1 point per $10 spent
        $customer.addLoyaltyPoints(points);
        System.out.println("Awarded " + points + " loyalty points to " + $customer.getFullName());
end

rule "Birthday Bonus Points"
    when
        $customer : Customer(
            dateOfBirth != null,
            dateOfBirth.getMonthValue() == java.time.LocalDate.now().getMonthValue(),
            dateOfBirth.getDayOfMonth() == java.time.LocalDate.now().getDayOfMonth()
        )
    then
        $customer.addLoyaltyPoints(200); // Birthday bonus
        System.out.println("Happy Birthday! Awarded 200 bonus points to " + $customer.getFullName());
end

rule "Inactive Customer Alert"
    when
        $customer : Customer(
            isActive() == true,
            orders.size() == 0 ||
            orders.stream().noneMatch(order ->
                order.getOrderDate().isAfter(java.time.LocalDateTime.now().minusMonths(6))
            )
        )
    then
        System.out.println("Alert: Customer " + $customer.getFullName() + " has been inactive for 6+ months");
        // Could trigger re-engagement campaign
end

rule "High Value Customer Recognition"
    when
        $customer : Customer(
            totalSpent > 25000.0,
            customerType != CustomerType.VIP
        )
    then
        $customer.setCustomerType(CustomerType.VIP);
        $customer.addLoyaltyPoints(2000); // Special recognition bonus
        System.out.println("High value customer " + $customer.getFullName() + " automatically upgraded to VIP");
end

==================================================

Enter your modification requirements (press Ctrl+D or Ctrl+Z when finished):
increase birthday bonus to 3000 points^Z
^Z
Modifying rule... This may take a moment.

=== Modified Rule ===
package com.example.drools.rules;

import com.example.drools.model.Customer;
import com.example.drools.model.CustomerType;
import com.example.drools.model.Order;

// Customer loyalty and tier upgrade rules

rule "Upgrade to Premium Customer"
    when
        $customer : Customer(
            customerType == CustomerType.REGULAR,
            totalSpent > 5000.0,
            loyaltyPoints > 1000
        )
    then
        $customer.setCustomerType(CustomerType.PREMIUM);
        $customer.addLoyaltyPoints(500); // Bonus points for upgrade
        System.out.println("Customer " + $customer.getFullName() + " upgraded to Premium");
end

rule "Upgrade to VIP Customer"
    when
        $customer : Customer(
            customerType == CustomerType.PREMIUM,
            totalSpent > 15000.0,
            loyaltyPoints > 5000
        )
    then
        $customer.setCustomerType(CustomerType.VIP);
        $customer.addLoyaltyPoints(1000); // Bonus points for VIP upgrade
        System.out.println("Customer " + $customer.getFullName() + " upgraded to VIP");
end

rule "Award Loyalty Points for Order"
    when
        $order : Order(status == com.example.drools.model.OrderStatus.DELIVERED)
        $customer : Customer(id == $order.customerId)
    then
        int points = (int) ($order.getTotalAmount() / 10); // 1 point per $10 spent
        $customer.addLoyaltyPoints(points);
        System.out.println("Awarded " + points + " loyalty points to " + $customer.getFullName());
end

rule "Birthday Bonus Points"
    when
        $customer : Customer(
            dateOfBirth != null,
            dateOfBirth.getMonthValue() == java.time.LocalDate.now().getMonthValue(),
            dateOfBirth.getDayOfMonth() == java.time.LocalDate.now().getDayOfMonth()
        )
    then
        // Increased birthday bonus to 3000 points as per requirement
        $customer.addLoyaltyPoints(3000); // Birthday bonus
        System.out.println("Happy Birthday! Awarded 3000 bonus points to " + $customer.getFullName());
end

rule "Inactive Customer Alert"
    when
        $customer : Customer(
            isActive() == true,
            orders.size() == 0 ||
            orders.stream().noneMatch(order ->
                order.getOrderDate().isAfter(java.time.LocalDateTime.now().minusMonths(6))
            )
        )
    then
        System.out.println("Alert: Customer " + $customer.getFullName() + " has been inactive for 6+ months");
        // Could trigger re-engagement campaign
end

rule "High Value Customer Recognition"
    when
        $customer : Customer(
            totalSpent > 25000.0,
            customerType != CustomerType.VIP
        )
    then
        $customer.setCustomerType(CustomerType.VIP);
        $customer.addLoyaltyPoints(2000); // Special recognition bonus
        System.out.println("High value customer " + $customer.getFullName() + " automatically upgraded to VIP");
end
==================================================

Save this modified rule? (y/n): y
Original rule backed up to: C:\Users\ganes\Downloads\tkinter-drl-system\example-springboot-project\src\main\resources\rules\customer-loyalty.drl.bak
Modified rule saved to: C:\Users\ganes\Downloads\tkinter-drl-system\example-springboot-project\src\main\resources\rules\customer-loyalty.drl
```

### 3. Direct Command Example

```bash
# Generate a rule with immediate requirements
drl generate --requirements "Create a rule that applies 10% discount when cart total > $100 and customer is premium" --output discount_rule.drl

# Modify a rule with specific requirements
drl modify validation.drl --requirements "Add email format validation using regex pattern"
```

## Best Practices

1. **Repository Structure**:
   - Keep Java models in clear package structure
   - Organize DRL files by business domain
   - Use consistent naming conventions

2. **Context Management**:
   - Rescan after major repository changes
   - Use `context` command to verify loaded information

3. **Rate Limiting**:
   - Large repositories may take time to process
   - Monitor token usage in verbose mode

4. **Modification Workflow**:
   - Always review generated changes
   - Use version control alongside the tool
   - Keep modification requirements specific and clear

## Troubleshooting

**Error: API rate limit exceeded**
- The system automatically handles rate limiting
- Wait a minute and try again
- Larger contexts may require more time to process

**Error: No DRL files found**
- Verify your repository path
- Ensure files have .drl extension
- Check file permissions

**Error: Invalid API key**
- Verify your Groq API key
- Use `config set-api-key` to update

## License

[MIT License](LICENSE)
```

This README provides:
1. Comprehensive feature overview
2. Technical details about token management
3. Quick start guide
4. Complete command reference
5. Practical examples
6. Best practices
7. Troubleshooting tips

