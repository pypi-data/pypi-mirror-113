Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var roleSelectControl_1 = tslib_1.__importDefault(require("app/components/roleSelectControl"));
var iconClose_1 = require("app/icons/iconClose");
var locale_1 = require("app/locale");
var renderEmailValue_1 = tslib_1.__importDefault(require("./renderEmailValue"));
function ValueComponent(props, inviteStatus) {
    return renderEmailValue_1.default(inviteStatus[props.data.value], props);
}
function mapToOptions(values) {
    return values.map(function (value) { return ({ value: value, label: value }); });
}
var InviteRowControl = /** @class */ (function (_super) {
    tslib_1.__extends(InviteRowControl, _super);
    function InviteRowControl() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { inputValue: '' };
        _this.handleInputChange = function (inputValue) {
            _this.setState({ inputValue: inputValue });
        };
        _this.handleKeyDown = function (event) {
            var _a = _this.props, onChangeEmails = _a.onChangeEmails, emails = _a.emails;
            var inputValue = _this.state.inputValue;
            switch (event.key) {
                case 'Enter':
                case ',':
                case ' ':
                    onChangeEmails(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(mapToOptions(emails))), [{ label: inputValue, value: inputValue }]));
                    _this.setState({ inputValue: '' });
                    event.preventDefault();
                    break;
                default:
                // do nothing.
            }
        };
        return _this;
    }
    InviteRowControl.prototype.render = function () {
        var _a = this.props, className = _a.className, disabled = _a.disabled, emails = _a.emails, role = _a.role, teams = _a.teams, roleOptions = _a.roleOptions, roleDisabledUnallowed = _a.roleDisabledUnallowed, teamOptions = _a.teamOptions, inviteStatus = _a.inviteStatus, onRemove = _a.onRemove, onChangeEmails = _a.onChangeEmails, onChangeRole = _a.onChangeRole, onChangeTeams = _a.onChangeTeams, disableRemove = _a.disableRemove, theme = _a.theme;
        return (<div className={className}>
        <selectControl_1.default data-test-id="select-emails" disabled={disabled} placeholder={locale_1.t('Enter one or more emails')} inputValue={this.state.inputValue} value={emails} components={{
                MultiValue: function (props) {
                    return ValueComponent(props, inviteStatus);
                },
                DropdownIndicator: function () { return null; },
            }} options={mapToOptions(emails)} onBlur={function (e) {
                return e.target.value &&
                    onChangeEmails(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(mapToOptions(emails))), [
                        { label: e.target.value, value: e.target.value },
                    ]));
            }} styles={getStyles(theme, inviteStatus)} onInputChange={this.handleInputChange} onKeyDown={this.handleKeyDown} onBlurResetsInput={false} onCloseResetsInput={false} onChange={onChangeEmails} multiple creatable clearable menuIsOpen={false}/>
        <roleSelectControl_1.default data-test-id="select-role" disabled={disabled} value={role} roles={roleOptions} disableUnallowed={roleDisabledUnallowed} onChange={onChangeRole}/>
        <selectControl_1.default data-test-id="select-teams" disabled={disabled} placeholder={locale_1.t('Add to teams\u2026')} value={teams} options={teamOptions.map(function (_a) {
                var slug = _a.slug;
                return ({
                    value: slug,
                    label: "#" + slug,
                });
            })} onChange={onChangeTeams} multiple clearable/>
        <button_1.default borderless icon={<iconClose_1.IconClose />} size="zero" onClick={onRemove} disabled={disableRemove}/>
      </div>);
    };
    return InviteRowControl;
}(React.Component));
/**
 * The email select control has custom selected item states as items
 * show their delivery status after the form is submitted.
 */
function getStyles(theme, inviteStatus) {
    return {
        multiValue: function (provided, _a) {
            var data = _a.data;
            var status = inviteStatus[data.value];
            return tslib_1.__assign(tslib_1.__assign({}, provided), ((status === null || status === void 0 ? void 0 : status.error)
                ? {
                    color: theme.red300,
                    border: "1px solid " + theme.red300,
                    backgroundColor: theme.red100,
                }
                : {}));
        },
        multiValueLabel: function (provided, _a) {
            var data = _a.data;
            var status = inviteStatus[data.value];
            return tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, provided), { pointerEvents: 'all' }), ((status === null || status === void 0 ? void 0 : status.error) ? { color: theme.red300 } : {}));
        },
        multiValueRemove: function (provided, _a) {
            var data = _a.data;
            var status = inviteStatus[data.value];
            return tslib_1.__assign(tslib_1.__assign({}, provided), ((status === null || status === void 0 ? void 0 : status.error)
                ? {
                    borderLeft: "1px solid " + theme.red300,
                    ':hover': { backgroundColor: theme.red100, color: theme.red300 },
                }
                : {}));
        },
    };
}
exports.default = react_1.withTheme(InviteRowControl);
//# sourceMappingURL=inviteRowControl.jsx.map