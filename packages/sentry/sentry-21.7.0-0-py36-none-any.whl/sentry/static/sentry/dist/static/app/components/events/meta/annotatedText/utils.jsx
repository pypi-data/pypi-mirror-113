Object.defineProperty(exports, "__esModule", { value: true });
exports.getTooltipText = void 0;
var locale_1 = require("app/locale");
var REMARKS = {
    a: 'Annotated',
    x: 'Removed',
    s: 'Replaced',
    m: 'Masked',
    p: 'Pseudonymized',
    e: 'Encrypted',
};
var KNOWN_RULES = {
    '!limit': 'size limits',
    '!raw': 'raw payload',
    '!config': 'SDK configuration',
};
function getTooltipText(_a) {
    var _b = _a.remark, remark = _b === void 0 ? '' : _b, _c = _a.rule_id, rule = _c === void 0 ? '' : _c;
    var remark_title = REMARKS[remark];
    var rule_title = KNOWN_RULES[rule] || locale_1.t('PII rule "%s"', rule);
    if (remark_title) {
        return locale_1.t('%s because of %s', remark_title, rule_title);
    }
    return rule_title;
}
exports.getTooltipText = getTooltipText;
//# sourceMappingURL=utils.jsx.map