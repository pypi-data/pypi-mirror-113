Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var types_1 = require("../../types");
var utils_1 = require("../utils");
var eventIdFieldStatusIcon_1 = tslib_1.__importDefault(require("./eventIdFieldStatusIcon"));
var EventIdField = /** @class */ (function (_super) {
    tslib_1.__extends(EventIdField, _super);
    function EventIdField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = tslib_1.__assign({}, _this.props.eventId);
        _this.handleChange = function (event) {
            var eventId = event.target.value.replace(/-/g, '').trim();
            if (eventId !== _this.state.value) {
                _this.setState({
                    value: eventId,
                    status: types_1.EventIdStatus.UNDEFINED,
                });
            }
        };
        _this.handleBlur = function (event) {
            event.preventDefault();
            if (_this.isEventIdValid()) {
                _this.props.onUpdateEventId(_this.state.value);
            }
        };
        _this.handleKeyDown = function (event) {
            var keyCode = event.keyCode;
            if (keyCode === 13 && _this.isEventIdValid()) {
                _this.props.onUpdateEventId(_this.state.value);
            }
        };
        _this.handleClickIconClose = function () {
            _this.setState({
                value: '',
                status: types_1.EventIdStatus.UNDEFINED,
            });
        };
        return _this;
    }
    EventIdField.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual_1.default(prevProps.eventId, this.props.eventId)) {
            this.loadState();
        }
    };
    EventIdField.prototype.loadState = function () {
        this.setState(tslib_1.__assign({}, this.props.eventId));
    };
    EventIdField.prototype.getErrorMessage = function () {
        var status = this.state.status;
        switch (status) {
            case types_1.EventIdStatus.INVALID:
                return locale_1.t('This event ID is invalid.');
            case types_1.EventIdStatus.ERROR:
                return locale_1.t('An error occurred while fetching the suggestions based on this event ID.');
            case types_1.EventIdStatus.NOT_FOUND:
                return locale_1.t('The chosen event ID was not found in projects you have access to.');
            default:
                return undefined;
        }
    };
    EventIdField.prototype.isEventIdValid = function () {
        var _a = this.state, value = _a.value, status = _a.status;
        if (value && value.length !== 32) {
            if (status !== types_1.EventIdStatus.INVALID) {
                utils_1.saveToSourceGroupData({ value: value, status: status });
                this.setState({ status: types_1.EventIdStatus.INVALID });
            }
            return false;
        }
        return true;
    };
    EventIdField.prototype.render = function () {
        var disabled = this.props.disabled;
        var _a = this.state, value = _a.value, status = _a.status;
        return (<field_1.default data-test-id="event-id-field" label={locale_1.t('Event ID (Optional)')} help={locale_1.t('Providing an event ID will automatically provide you a list of suggested sources')} inline={false} error={this.getErrorMessage()} flexibleControlStateSize stacked showHelpInTooltip>
        <FieldWrapper>
          <StyledInput type="text" name="eventId" disabled={disabled} value={value} placeholder={locale_1.t('XXXXXXXXXXXXXX')} onChange={this.handleChange} onKeyDown={this.handleKeyDown} onBlur={this.handleBlur}/>
          <Status>
            <eventIdFieldStatusIcon_1.default onClickIconClose={this.handleClickIconClose} status={status}/>
          </Status>
        </FieldWrapper>
      </field_1.default>);
    };
    return EventIdField;
}(React.Component));
exports.default = EventIdField;
var StyledInput = styled_1.default(input_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  font-weight: 400;\n  input {\n    padding-right: ", ";\n  }\n  margin-bottom: 0;\n"], ["\n  flex: 1;\n  font-weight: 400;\n  input {\n    padding-right: ", ";\n  }\n  margin-bottom: 0;\n"])), space_1.default(1.5));
var Status = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 40px;\n  position: absolute;\n  right: ", ";\n  top: 0;\n  display: flex;\n  align-items: center;\n"], ["\n  height: 40px;\n  position: absolute;\n  right: ", ";\n  top: 0;\n  display: flex;\n  align-items: center;\n"])), space_1.default(1.5));
var FieldWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n  align-items: center;\n"], ["\n  position: relative;\n  display: flex;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventIdField.jsx.map