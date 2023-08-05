Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var autoSelectText_1 = tslib_1.__importDefault(require("app/components/autoSelectText"));
var ShortId = /** @class */ (function (_super) {
    tslib_1.__extends(ShortId, _super);
    function ShortId() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ShortId.prototype.render = function () {
        var _a = this.props, shortId = _a.shortId, avatar = _a.avatar;
        if (!shortId) {
            return null;
        }
        return (<StyledShortId {...this.props}>
        {avatar}
        <StyledAutoSelectText avatar={!!avatar}>{shortId}</StyledAutoSelectText>
      </StyledShortId>);
    };
    return ShortId;
}(React.Component));
exports.default = ShortId;
var StyledShortId = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  font-family: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"])), function (p) { return p.theme.text.familyMono; });
var StyledAutoSelectText = styled_1.default(autoSelectText_1.default, { shouldForwardProp: is_prop_valid_1.default })(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  min-width: 0;\n"], ["\n  margin-left: ", ";\n  min-width: 0;\n"])), function (p) { return p.avatar && '0.5em'; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=shortId.jsx.map