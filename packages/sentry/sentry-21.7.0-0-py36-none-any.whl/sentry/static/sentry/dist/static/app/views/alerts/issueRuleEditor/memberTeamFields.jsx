Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var panels_1 = require("app/components/panels");
var selectMembers_1 = tslib_1.__importDefault(require("app/components/selectMembers"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var MemberTeamFields = /** @class */ (function (_super) {
    tslib_1.__extends(MemberTeamFields, _super);
    function MemberTeamFields() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function (attribute, newValue) {
            var _a;
            var _b = _this.props, onChange = _b.onChange, ruleData = _b.ruleData;
            if (newValue === ruleData[attribute]) {
                return;
            }
            var newData = tslib_1.__assign(tslib_1.__assign({}, ruleData), (_a = {}, _a[attribute] = newValue, _a));
            /**
             * TargetIdentifiers between the targetTypes are not unique, and may wrongly map to something that has not been
             * selected. E.g. A member and project can both have the `targetIdentifier`, `'2'`. Hence we clear the identifier.
             **/
            if (attribute === 'targetType') {
                newData.targetIdentifier = '';
            }
            onChange(newData);
        };
        _this.handleChangeActorType = function (optionRecord) {
            _this.handleChange('targetType', optionRecord.value);
        };
        _this.handleChangeActorId = function (optionRecord) {
            _this.handleChange('targetIdentifier', optionRecord.value);
        };
        return _this;
    }
    MemberTeamFields.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, loading = _a.loading, project = _a.project, organization = _a.organization, ruleData = _a.ruleData, memberValue = _a.memberValue, teamValue = _a.teamValue, options = _a.options;
        var teamSelected = ruleData.targetType === teamValue;
        var memberSelected = ruleData.targetType === memberValue;
        var selectControlStyles = {
            control: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { minHeight: '28px', height: '28px' })); },
        };
        return (<PanelItemGrid>
        <selectControl_1.default isClearable={false} isDisabled={disabled || loading} value={ruleData.targetType} styles={selectControlStyles} options={options} onChange={this.handleChangeActorType}/>
        {teamSelected || memberSelected ? (<selectMembers_1.default disabled={disabled} key={teamSelected ? teamValue : memberValue} showTeam={teamSelected} project={project} organization={organization} 
            // The value from the endpoint is of type `number`, `SelectMembers` require value to be of type `string`
            value={"" + ruleData.targetIdentifier} styles={selectControlStyles} onChange={this.handleChangeActorId}/>) : (<span />)}
      </PanelItemGrid>);
    };
    return MemberTeamFields;
}(React.Component));
var PanelItemGrid = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 200px 200px;\n  padding: 0;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 200px 200px;\n  padding: 0;\n  align-items: center;\n  grid-gap: ", ";\n"])), space_1.default(2));
exports.default = MemberTeamFields;
var templateObject_1;
//# sourceMappingURL=memberTeamFields.jsx.map