Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var button_1 = tslib_1.__importDefault(require("app/components/actions/button"));
var menuHeader_1 = tslib_1.__importDefault(require("app/components/actions/menuHeader"));
var menuItemActionLink_1 = tslib_1.__importDefault(require("app/components/actions/menuItemActionLink"));
var button_2 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
function DeleteAction(_a) {
    var disabled = _a.disabled, project = _a.project, organization = _a.organization, onDiscard = _a.onDiscard, onDelete = _a.onDelete;
    function renderDiscardDisabled(_a) {
        var children = _a.children, props = tslib_1.__rest(_a, ["children"]);
        return children(tslib_1.__assign(tslib_1.__assign({}, props), { renderDisabled: function (_a) {
                var features = _a.features;
                return (<featureDisabled_1.default alert featureName="Discard and Delete" features={features}/>);
            } }));
    }
    function renderDiscardModal(_a) {
        var Body = _a.Body, Footer = _a.Footer, closeModal = _a.closeModal;
        return (<feature_1.default features={['projects:discard-groups']} hookName="feature-disabled:discard-groups" organization={organization} project={project} renderDisabled={renderDiscardDisabled}>
        {function (_a) {
                var hasFeature = _a.hasFeature, renderDisabled = _a.renderDisabled, props = tslib_1.__rest(_a, ["hasFeature", "renderDisabled"]);
                return (<react_1.Fragment>
            <Body>
              {!hasFeature &&
                        typeof renderDisabled === 'function' &&
                        renderDisabled(tslib_1.__assign(tslib_1.__assign({}, props), { hasFeature: hasFeature, children: null }))}
              {locale_1.t("Discarding this event will result in the deletion of most data associated with this issue and future events being discarded before reaching your stream. Are you sure you wish to continue?")}
            </Body>
            <Footer>
              <button_2.default onClick={closeModal}>{locale_1.t('Cancel')}</button_2.default>
              <button_2.default style={{ marginLeft: space_1.default(1) }} priority="primary" onClick={onDiscard} disabled={!hasFeature}>
                {locale_1.t('Discard Future Events')}
              </button_2.default>
            </Footer>
          </react_1.Fragment>);
            }}
      </feature_1.default>);
    }
    function openDiscardModal() {
        modal_1.openModal(renderDiscardModal);
        analytics_1.analytics('feature.discard_group.modal_opened', {
            org_id: parseInt(organization.id, 10),
        });
    }
    return (<buttonBar_1.default merged>
      <confirm_1.default message={locale_1.t('Deleting this issue is permanent. Are you sure you wish to continue?')} onConfirm={onDelete} disabled={disabled}>
        <DeleteButton disabled={disabled} label={locale_1.t('Delete issue')} icon={<icons_1.IconDelete size="xs"/>}/>
      </confirm_1.default>
      <dropdownLink_1.default caret={false} disabled={disabled} customTitle={<button_1.default disabled={disabled} label={locale_1.t('More delete options')} icon={<icons_1.IconChevron direction="down" size="xs"/>}/>}>
        <menuHeader_1.default>{locale_1.t('Delete & Discard')}</menuHeader_1.default>
        <menuItemActionLink_1.default title="" onAction={openDiscardModal}>
          {locale_1.t('Delete and discard future events')}
        </menuItemActionLink_1.default>
      </dropdownLink_1.default>
    </buttonBar_1.default>);
}
var DeleteButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return !p.disabled &&
        "\n  &:hover {\n    background-color: " + p.theme.button.danger.background + ";\n    color: " + p.theme.button.danger.color + ";\n    border-color: " + p.theme.button.danger.border + ";\n  }\n  ";
});
exports.default = DeleteAction;
var templateObject_1;
//# sourceMappingURL=deleteAction.jsx.map