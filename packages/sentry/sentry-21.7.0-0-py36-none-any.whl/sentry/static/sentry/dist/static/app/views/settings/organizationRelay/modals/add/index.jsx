Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var modalManager_1 = tslib_1.__importDefault(require("../modalManager"));
var item_1 = tslib_1.__importDefault(require("./item"));
var terminal_1 = tslib_1.__importDefault(require("./terminal"));
var Add = /** @class */ (function (_super) {
    tslib_1.__extends(Add, _super);
    function Add() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Add.prototype.getTitle = function () {
        return locale_1.t('Register Key');
    };
    Add.prototype.getBtnSaveLabel = function () {
        return locale_1.t('Register');
    };
    Add.prototype.getData = function () {
        var savedRelays = this.props.savedRelays;
        var trustedRelays = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(savedRelays)), [this.state.values]);
        return { trustedRelays: trustedRelays };
    };
    Add.prototype.getContent = function () {
        return (<StyledList symbol="colored-numeric">
        <item_1.default title={locale_1.tct('Initialize the configuration. [link: Learn how]', {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/relay/getting-started/#initializing-configuration"/>),
            })} subtitle={locale_1.t('Within your terminal:')}>
          <terminal_1.default command="relay config init"/>
        </item_1.default>
        <item_1.default title={locale_1.tct('Go to the file [jsonFile: credentials.json] to find the public key and enter it below.', {
                jsonFile: (<externalLink_1.default href="https://docs.sentry.io/product/relay/getting-started/#registering-relay-with-sentry"/>),
            })}>
          {_super.prototype.getForm.call(this)}
        </item_1.default>
      </StyledList>);
    };
    return Add;
}(modalManager_1.default));
exports.default = Add;
var StyledList = styled_1.default(list_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(3));
var templateObject_1;
//# sourceMappingURL=index.jsx.map