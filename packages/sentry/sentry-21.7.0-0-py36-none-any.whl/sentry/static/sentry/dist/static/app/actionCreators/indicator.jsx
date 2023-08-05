Object.defineProperty(exports, "__esModule", { value: true });
exports.saveOnBlurUndoMessage = exports.addSuccessMessage = exports.addErrorMessage = exports.addLoadingMessage = exports.addMessage = exports.clearIndicators = exports.removeIndicator = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var indicatorActions_1 = tslib_1.__importDefault(require("app/actions/indicatorActions"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
// Removes a single indicator
function removeIndicator(indicator) {
    indicatorActions_1.default.remove(indicator);
}
exports.removeIndicator = removeIndicator;
// Clears all indicators
function clearIndicators() {
    indicatorActions_1.default.clear();
}
exports.clearIndicators = clearIndicators;
// Note previous IndicatorStore.add behavior was to default to "loading" if no type was supplied
function addMessage(msg, type, options) {
    if (options === void 0) { options = {}; }
    var optionsDuration = options.duration, append = options.append, rest = tslib_1.__rest(options, ["duration", "append"]);
    // XXX: Debug for https://sentry.io/organizations/sentry/issues/1595204979/
    if (
    // @ts-expect-error
    typeof (msg === null || msg === void 0 ? void 0 : msg.message) !== 'undefined' &&
        // @ts-expect-error
        typeof (msg === null || msg === void 0 ? void 0 : msg.code) !== 'undefined' &&
        // @ts-expect-error
        typeof (msg === null || msg === void 0 ? void 0 : msg.extra) !== 'undefined') {
        Sentry.captureException(new Error('Attempt to XHR response to Indicators'));
    }
    // use default only if undefined, as 0 is a valid duration
    var duration = typeof optionsDuration === 'undefined' ? constants_1.DEFAULT_TOAST_DURATION : optionsDuration;
    var action = append ? 'append' : 'replace';
    // XXX: This differs from `IndicatorStore.add` since it won't return the indicator that is created
    // because we are firing an action. You can just add a new message and it will, by default,
    // replace active indicator
    indicatorActions_1.default[action](msg, type, tslib_1.__assign(tslib_1.__assign({}, rest), { duration: duration }));
}
exports.addMessage = addMessage;
function addMessageWithType(type) {
    return function (msg, options) { return addMessage(msg, type, options); };
}
function addLoadingMessage(msg, options) {
    if (msg === void 0) { msg = locale_1.t('Saving changes...'); }
    return addMessageWithType('loading')(msg, options);
}
exports.addLoadingMessage = addLoadingMessage;
function addErrorMessage(msg, options) {
    return addMessageWithType('error')(msg, options);
}
exports.addErrorMessage = addErrorMessage;
function addSuccessMessage(msg, options) {
    return addMessageWithType('success')(msg, options);
}
exports.addSuccessMessage = addSuccessMessage;
var PRETTY_VALUES = new Map([
    ['', '<empty>'],
    [null, '<none>'],
    [undefined, '<unset>'],
    // if we don't cast as any, then typescript complains because booleans are not valid keys
    [true, 'enabled'],
    [false, 'disabled'],
]);
// Transform form values into a string
// Otherwise bool values will not get rendered and empty strings look like a bug
var prettyFormString = function (val, model, fieldName) {
    var descriptor = model.fieldDescriptor.get(fieldName);
    if (descriptor && typeof descriptor.formatMessageValue === 'function') {
        var initialData = model.initialData;
        // XXX(epurkhsier): We pass the "props" as the descriptor and initialData.
        // This isn't necessarily all of the props of the form field, but should
        // make up a good portion needed for formatting.
        return descriptor.formatMessageValue(val, tslib_1.__assign(tslib_1.__assign({}, descriptor), { initialData: initialData }));
    }
    if (PRETTY_VALUES.has(val)) {
        return PRETTY_VALUES.get(val);
    }
    return typeof val === 'object' ? val : String(val);
};
/**
 * This will call an action creator to generate a "Toast" message that
 * notifies user the field that changed with its previous and current values.
 *
 * Also allows for undo
 */
function saveOnBlurUndoMessage(change, model, fieldName) {
    if (!model) {
        return;
    }
    var label = model.getDescriptor(fieldName, 'label');
    if (!label) {
        return;
    }
    var prettifyValue = function (val) { return prettyFormString(val, model, fieldName); };
    // Hide the change text when formatMessageValue is explicitly set to false
    var showChangeText = model.getDescriptor(fieldName, 'formatMessageValue') !== false;
    addSuccessMessage(locale_1.tct(showChangeText
        ? 'Changed [fieldName] from [oldValue] to [newValue]'
        : 'Changed [fieldName]', {
        root: <MessageContainer />,
        fieldName: <FieldName>{label}</FieldName>,
        oldValue: <FormValue>{prettifyValue(change.old)}</FormValue>,
        newValue: <FormValue>{prettifyValue(change.new)}</FormValue>,
    }), {
        modelArg: {
            model: model,
            id: fieldName,
            undo: function () {
                if (!model || !fieldName) {
                    return;
                }
                var oldValue = model.getValue(fieldName);
                var didUndo = model.undo();
                var newValue = model.getValue(fieldName);
                if (!didUndo) {
                    return;
                }
                if (!label) {
                    return;
                }
                // `saveField` can return null if it can't save
                var saveResult = model.saveField(fieldName, newValue);
                if (!saveResult) {
                    addErrorMessage(locale_1.tct(showChangeText
                        ? 'Unable to restore [fieldName] from [oldValue] to [newValue]'
                        : 'Unable to restore [fieldName]', {
                        root: <MessageContainer />,
                        fieldName: <FieldName>{label}</FieldName>,
                        oldValue: <FormValue>{prettifyValue(oldValue)}</FormValue>,
                        newValue: <FormValue>{prettifyValue(newValue)}</FormValue>,
                    }));
                    return;
                }
                saveResult.then(function () {
                    addMessage(locale_1.tct(showChangeText
                        ? 'Restored [fieldName] from [oldValue] to [newValue]'
                        : 'Restored [fieldName]', {
                        root: <MessageContainer />,
                        fieldName: <FieldName>{label}</FieldName>,
                        oldValue: <FormValue>{prettifyValue(oldValue)}</FormValue>,
                        newValue: <FormValue>{prettifyValue(newValue)}</FormValue>,
                    }), 'undo', {
                        duration: constants_1.DEFAULT_TOAST_DURATION,
                    });
                });
            },
        },
    });
}
exports.saveOnBlurUndoMessage = saveOnBlurUndoMessage;
var FormValue = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-style: italic;\n  margin: 0 ", ";\n"], ["\n  font-style: italic;\n  margin: 0 ", ";\n"])), space_1.default(0.5));
var FieldName = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  margin: 0 ", ";\n"], ["\n  font-weight: bold;\n  margin: 0 ", ";\n"])), space_1.default(0.5));
var MessageContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=indicator.jsx.map