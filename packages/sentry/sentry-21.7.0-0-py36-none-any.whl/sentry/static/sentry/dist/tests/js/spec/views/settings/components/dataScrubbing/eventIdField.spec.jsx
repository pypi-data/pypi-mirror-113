Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var eventIdField_1 = tslib_1.__importDefault(require("app/views/settings/components/dataScrubbing/modals/form/eventIdField"));
var types_1 = require("app/views/settings/components/dataScrubbing/types");
var handleUpdateEventId = jest.fn();
var eventIdValue = '887ab369df634e74aea708bcafe1a175';
function renderComponent(_a) {
    var _b = _a.value, value = _b === void 0 ? eventIdValue : _b, status = _a.status;
    return enzyme_1.mountWithTheme(<eventIdField_1.default onUpdateEventId={handleUpdateEventId} eventId={{ value: value, status: status }}/>);
}
describe('EventIdField', function () {
    it('default render', function () {
        var wrapper = renderComponent({ value: '', status: types_1.EventIdStatus.UNDEFINED });
        var eventIdField = wrapper.find('Field');
        expect(eventIdField.exists()).toBe(true);
        expect(eventIdField.find('FieldLabel').text()).toEqual('Event ID (Optional)');
        var eventIdFieldHelp = 'Providing an event ID will automatically provide you a list of suggested sources';
        expect(eventIdField.find('QuestionTooltip').prop('title')).toEqual(eventIdFieldHelp);
        expect(eventIdField.find('Tooltip').prop('title')).toEqual(eventIdFieldHelp);
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual('');
        expect(eventIdFieldInput.prop('placeholder')).toEqual('XXXXXXXXXXXXXX');
        eventIdFieldInput.simulate('change', {
            target: { value: '887ab369df634e74aea708bcafe1a175' },
        });
        eventIdFieldInput.simulate('blur');
        expect(handleUpdateEventId).toHaveBeenCalled();
    });
    it('LOADING status', function () {
        var wrapper = renderComponent({ status: types_1.EventIdStatus.LOADING });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(0);
        expect(eventIdField.find('CloseIcon')).toHaveLength(0);
        expect(eventIdField.find('FormSpinner')).toHaveLength(1);
    });
    it('LOADED status', function () {
        var wrapper = renderComponent({ status: types_1.EventIdStatus.LOADED });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(0);
        expect(eventIdField.find('CloseIcon')).toHaveLength(0);
        var iconCheckmark = eventIdField.find('IconCheckmark');
        expect(iconCheckmark).toHaveLength(1);
        var iconCheckmarkColor = iconCheckmark.prop('color');
        expect(theme_1.default[iconCheckmarkColor]).toBe(theme_1.default.green300);
    });
    it('ERROR status', function () {
        var wrapper = renderComponent({ status: types_1.EventIdStatus.ERROR });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(1);
        var closeIcon = eventIdField.find('CloseIcon');
        expect(closeIcon).toHaveLength(1);
        expect(closeIcon.find('Tooltip').prop('title')).toEqual('Clear event ID');
        var fieldErrorReason = eventIdField.find('FieldErrorReason');
        expect(fieldErrorReason).toHaveLength(1);
        expect(fieldErrorReason.text()).toEqual('An error occurred while fetching the suggestions based on this event ID.');
    });
    it('INVALID status', function () {
        var wrapper = renderComponent({ status: types_1.EventIdStatus.INVALID });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(1);
        expect(eventIdField.find('CloseIcon')).toHaveLength(1);
        var fieldErrorReason = eventIdField.find('FieldErrorReason');
        expect(fieldErrorReason).toHaveLength(1);
        expect(fieldErrorReason.text()).toEqual('This event ID is invalid.');
    });
    it('NOTFOUND status', function () {
        var wrapper = renderComponent({ status: types_1.EventIdStatus.NOT_FOUND });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(1);
        expect(eventIdField.find('CloseIcon')).toHaveLength(1);
        var fieldErrorReason = eventIdField.find('FieldErrorReason');
        expect(fieldErrorReason).toHaveLength(1);
        expect(fieldErrorReason.text()).toEqual('The chosen event ID was not found in projects you have access to.');
    });
});
//# sourceMappingURL=eventIdField.spec.jsx.map