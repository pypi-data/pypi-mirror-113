Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var panels_1 = require("app/components/panels");
var selectMembers_1 = tslib_1.__importDefault(require("app/components/selectMembers"));
var locale_1 = require("app/locale");
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var textField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textField"));
var RuleNameOwnerForm = /** @class */ (function (_super) {
    tslib_1.__extends(RuleNameOwnerForm, _super);
    function RuleNameOwnerForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RuleNameOwnerForm.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, project = _a.project, organization = _a.organization, userTeamIds = _a.userTeamIds;
        return (<panels_1.Panel>
        <panels_1.PanelBody>
          <textField_1.default disabled={disabled} name="name" label={locale_1.t('Rule Name')} help={locale_1.t('Add a name so it’s easy to find later.')} placeholder={locale_1.t('Something really bad happened')} required/>

          <formField_1.default name="owner" label={locale_1.t('Team')} help={locale_1.t('The team that can edit this alert.')} disabled={disabled}>
            {function (_a) {
                var model = _a.model;
                var owner = model.getValue('owner');
                var ownerId = owner && owner.split(':')[1];
                var filteredTeamIds = new Set(userTeamIds);
                // Add the current team that owns the alert
                if (ownerId) {
                    filteredTeamIds.add(ownerId);
                }
                return (<selectMembers_1.default showTeam project={project} organization={organization} value={ownerId} onChange={function (_a) {
                        var value = _a.value;
                        var ownerValue = value && "team:" + value;
                        model.setValue('owner', ownerValue);
                    }} filteredTeamIds={filteredTeamIds} includeUnassigned disabled={disabled}/>);
            }}
          </formField_1.default>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return RuleNameOwnerForm;
}(react_1.PureComponent));
exports.default = RuleNameOwnerForm;
//# sourceMappingURL=ruleNameOwnerForm.jsx.map