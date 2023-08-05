Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var locale_1 = require("app/locale");
var redaction_1 = tslib_1.__importDefault(require("./redaction"));
// If you find yourself modifying this component to fix some tooltip bug,
// consider that `meta` is not properly passed into this component in the
// first place. It's much more likely that `withMeta` is buggy or improperly
// used than that this component has a bug.
var ValueElement = function (_a) {
    var _b, _c;
    var value = _a.value, meta = _a.meta;
    if (value && meta) {
        return <redaction_1.default>{value}</redaction_1.default>;
    }
    if ((_b = meta === null || meta === void 0 ? void 0 : meta.err) === null || _b === void 0 ? void 0 : _b.length) {
        return (<redaction_1.default withoutBackground>
        <i>{"<" + locale_1.t('invalid') + ">"}</i>
      </redaction_1.default>);
    }
    if ((_c = meta === null || meta === void 0 ? void 0 : meta.rem) === null || _c === void 0 ? void 0 : _c.length) {
        return (<redaction_1.default>
        <i>{"<" + locale_1.t('redacted') + ">"}</i>
      </redaction_1.default>);
    }
    if (React.isValidElement(value)) {
        return value;
    }
    return (<React.Fragment>
      {typeof value === 'object' || typeof value === 'boolean'
            ? JSON.stringify(value)
            : value}
    </React.Fragment>);
};
exports.default = ValueElement;
//# sourceMappingURL=valueElement.jsx.map