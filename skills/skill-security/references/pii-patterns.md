# PII Pattern Library

This file provides detection patterns for Personally Identifiable Information (PII) used by skill-security audits.

## High-Risk PII Patterns

### Email Addresses
```regex
[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}
```

### Phone Numbers (International)
```regex
(\+?[\d\s\-().]{7,15})
```

### Social Security / National ID Numbers
```regex
\b\d{3}-\d{2}-\d{4}\b        # SSN (US)
\b\d{11}\b                   # TR National ID (11 digits)
```

### Credit Card Numbers
```regex
\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b
```

### IP Addresses
```regex
\b(?:\d{1,3}\.){3}\d{1,3}\b
```

### API Keys / Secrets (Generic Heuristic)
```regex
(?i)(api[_\-]?key|secret|token|password|passwd|auth)["\s:=]+[A-Za-z0-9+/=_\-]{16,}
```

### JWT Tokens
```regex
eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+
```

## Audit Questions

When a skill handles user data:

- [ ] Is this data type covered by GDPR / KVKK / local privacy laws?
- [ ] Is the data encrypted in transit (TLS 1.2+) and at rest?
- [ ] Is the minimum necessary data collected (Data Minimization)?
- [ ] Is there a data retention policy and deletion mechanism?
- [ ] Could data from one user leak to another (multi-tenant risk)?
