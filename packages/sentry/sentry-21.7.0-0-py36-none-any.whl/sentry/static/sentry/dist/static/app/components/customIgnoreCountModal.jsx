Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var locale_1 = require("app/locale");
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var CustomIgnoreCountModal = /** @class */ (function (_super) {
    tslib_1.__extends(CustomIgnoreCountModal, _super);
    function CustomIgnoreCountModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            count: 100,
            window: null,
        };
        _this.handleSubmit = function () {
            var _a;
            var _b = _this.state, count = _b.count, window = _b.window;
            var _c = _this.props, countName = _c.countName, windowName = _c.windowName;
            var statusDetails = (_a = {}, _a[countName] = count, _a);
            if (window) {
                statusDetails[windowName] = window;
            }
            _this.props.onSelected(statusDetails);
            _this.props.closeModal();
        };
        _this.handleChange = function (name, value) {
            var _a;
            _this.setState((_a = {}, _a[name] = value, _a));
        };
        return _this;
    }
    CustomIgnoreCountModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Header = _a.Header, Footer = _a.Footer, Body = _a.Body, countLabel = _a.countLabel, label = _a.label, closeModal = _a.closeModal, windowChoices = _a.windowChoices;
        var _b = this.state, count = _b.count, window = _b.window;
        return (<react_1.Fragment>
        <Header>
          <h4>{label}</h4>
        </Header>
        <Body>
          <inputField_1.default inline={false} flexibleControlStateSize stacked label={countLabel} name="count" type="number" value={count} onChange={function (val) { return _this.handleChange('count', Number(val)); }} required placeholder={locale_1.t('e.g. 100')}/>
          <selectField_1.default inline={false} flexibleControlStateSize stacked label={locale_1.t('Time window')} value={window} name="window" onChange={function (val) { return _this.handleChange('window', val); }} choices={windowChoices} placeholder={locale_1.t('e.g. per hour')} allowClear help={locale_1.t('(Optional) If supplied, this rule will apply as a rate of change.')}/>
        </Body>
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default type="button" onClick={closeModal}>
              {locale_1.t('Cancel')}
            </button_1.default>
            <button_1.default type="button" priority="primary" onClick={this.handleSubmit}>
              {locale_1.t('Ignore')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </react_1.Fragment>);
    };
    return CustomIgnoreCountModal;
}(react_1.Component));
exports.default = CustomIgnoreCountModal;
//# sourceMappingURL=customIgnoreCountModal.jsx.map