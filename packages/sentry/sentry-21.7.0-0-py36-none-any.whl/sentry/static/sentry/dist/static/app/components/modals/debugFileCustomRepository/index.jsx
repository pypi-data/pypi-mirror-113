Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var debugFileSources_1 = require("app/data/debugFileSources");
var locale_1 = require("app/locale");
var fieldFromConfig_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/fieldFromConfig"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var appStoreConnect_1 = tslib_1.__importDefault(require("./appStoreConnect"));
var utils_1 = require("./utils");
function DebugFileCustomRepository(_a) {
    var Header = _a.Header, Body = _a.Body, Footer = _a.Footer, onSave = _a.onSave, sourceConfig = _a.sourceConfig, sourceType = _a.sourceType, _b = _a.params, orgId = _b.orgId, projectSlug = _b.projectId, location = _a.location, appStoreConnectContext = _a.appStoreConnectContext, closeModal = _a.closeModal;
    function handleSave(data) {
        onSave(tslib_1.__assign(tslib_1.__assign({}, data), { type: sourceType })).then(function () {
            closeModal();
            if (sourceType === 'appStoreConnect' &&
                (appStoreConnectContext === null || appStoreConnectContext === void 0 ? void 0 : appStoreConnectContext.updateAlertMessage)) {
                window.location.reload();
            }
        });
    }
    if (sourceType === 'appStoreConnect') {
        return (<appStoreConnect_1.default Header={Header} Body={Body} Footer={Footer} orgSlug={orgId} projectSlug={projectSlug} onSubmit={handleSave} initialData={sourceConfig} location={location} appStoreConnectContext={appStoreConnectContext}/>);
    }
    var fields = utils_1.getFormFields(sourceType);
    var initialData = utils_1.getInitialData(sourceConfig);
    return (<react_1.Fragment>
      <Header closeButton>
        {sourceConfig
            ? locale_1.tct('Update [name] Repository', { name: debugFileSources_1.getDebugSourceName(sourceType) })
            : locale_1.tct('Add [name] Repository', { name: debugFileSources_1.getDebugSourceName(sourceType) })}
      </Header>
      {fields && (<form_1.default allowUndo requireChanges initialData={initialData} onSubmit={handleSave} footerClass="modal-footer">
          {fields.map(function (field, i) { return (<fieldFromConfig_1.default key={field.name || i} field={field} inline={false} stacked/>); })}
        </form_1.default>)}
    </react_1.Fragment>);
}
exports.default = react_router_1.withRouter(DebugFileCustomRepository);
exports.modalCss = react_2.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  max-width: 680px;\n"], ["\n  width: 100%;\n  max-width: 680px;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map