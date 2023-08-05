Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var locale_1 = require("app/locale");
var Modal = function (_a) {
    var title = _a.title, onSave = _a.onSave, content = _a.content, disabled = _a.disabled, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, closeModal = _a.closeModal;
    return (<React.Fragment>
    <Header closeButton>{title}</Header>
    <Body>{content}</Body>
    <Footer>
      <buttonBar_1.default gap={1.5}>
        <button_1.default onClick={closeModal}>{locale_1.t('Cancel')}</button_1.default>
        <button_1.default onClick={onSave} disabled={disabled} priority="primary">
          {locale_1.t('Save Rule')}
        </button_1.default>
      </buttonBar_1.default>
    </Footer>
  </React.Fragment>);
};
exports.default = Modal;
//# sourceMappingURL=modal.jsx.map