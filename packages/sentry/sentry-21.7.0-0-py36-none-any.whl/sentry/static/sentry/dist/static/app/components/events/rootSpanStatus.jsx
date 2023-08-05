Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var RootSpanStatus = /** @class */ (function (_super) {
    tslib_1.__extends(RootSpanStatus, _super);
    function RootSpanStatus() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RootSpanStatus.prototype.getTransactionEvent = function () {
        var event = this.props.event;
        if (event.type === 'transaction') {
            return event;
        }
        return undefined;
    };
    RootSpanStatus.prototype.getRootSpanStatus = function () {
        var _a, _b;
        var event = this.getTransactionEvent();
        var DEFAULT = '\u2014';
        if (!event) {
            return DEFAULT;
        }
        var traceContext = (_a = event === null || event === void 0 ? void 0 : event.contexts) === null || _a === void 0 ? void 0 : _a.trace;
        return (_b = traceContext === null || traceContext === void 0 ? void 0 : traceContext.status) !== null && _b !== void 0 ? _b : DEFAULT;
    };
    RootSpanStatus.prototype.getHttpStatusCode = function () {
        var event = this.props.event;
        var tags = event.tags;
        if (!Array.isArray(tags)) {
            return '';
        }
        var tag = tags.find(function (tagObject) { return tagObject.key === 'http.status_code'; });
        if (!tag) {
            return '';
        }
        return tag.value;
    };
    RootSpanStatus.prototype.render = function () {
        var event = this.getTransactionEvent();
        if (!event) {
            return null;
        }
        var label = (this.getHttpStatusCode() + " " + this.getRootSpanStatus()).trim();
        return (<Container>
        <Header>
          <styles_1.SectionHeading>{locale_1.t('Status')}</styles_1.SectionHeading>
        </Header>
        <div>{label}</div>
      </Container>);
    };
    return RootSpanStatus;
}(react_1.Component));
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(4));
var Header = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
exports.default = RootSpanStatus;
var templateObject_1, templateObject_2;
//# sourceMappingURL=rootSpanStatus.jsx.map