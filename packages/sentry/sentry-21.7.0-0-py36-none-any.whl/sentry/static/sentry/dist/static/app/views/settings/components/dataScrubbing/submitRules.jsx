Object.defineProperty(exports, "__esModule", { value: true });
var types_1 = require("./types");
function getSubmitFormatRule(rule) {
    if (rule.type === types_1.RuleType.PATTERN && rule.method === types_1.MethodType.REPLACE) {
        return {
            type: rule.type,
            pattern: rule.pattern,
            redaction: {
                method: rule.method,
                text: rule === null || rule === void 0 ? void 0 : rule.placeholder,
            },
        };
    }
    if (rule.type === types_1.RuleType.PATTERN) {
        return {
            type: rule.type,
            pattern: rule.pattern,
            redaction: {
                method: rule.method,
            },
        };
    }
    if (rule.method === types_1.MethodType.REPLACE) {
        return {
            type: rule.type,
            redaction: {
                method: rule.method,
                text: rule === null || rule === void 0 ? void 0 : rule.placeholder,
            },
        };
    }
    return {
        type: rule.type,
        redaction: {
            method: rule.method,
        },
    };
}
function submitRules(api, endpoint, rules) {
    var applications = {};
    var submitFormatRules = {};
    for (var i = 0; i < rules.length; i++) {
        var rule = rules[i];
        var ruleId = String(i);
        submitFormatRules[ruleId] = getSubmitFormatRule(rule);
        if (!applications[rule.source]) {
            applications[rule.source] = [];
        }
        if (!applications[rule.source].includes(ruleId)) {
            applications[rule.source].push(ruleId);
        }
    }
    var piiConfig = { rules: submitFormatRules, applications: applications };
    return api.requestPromise(endpoint, {
        method: 'PUT',
        data: { relayPiiConfig: JSON.stringify(piiConfig) },
    });
}
exports.default = submitRules;
//# sourceMappingURL=submitRules.jsx.map