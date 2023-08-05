Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_select_1 = tslib_1.__importStar(require("react-select"));
var async_1 = tslib_1.__importDefault(require("react-select/async"));
var async_creatable_1 = tslib_1.__importDefault(require("react-select/async-creatable"));
var creatable_1 = tslib_1.__importDefault(require("react-select/creatable"));
var react_1 = require("@emotion/react");
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var convertFromSelect2Choices_1 = tslib_1.__importDefault(require("app/utils/convertFromSelect2Choices"));
function isGroupedOptions(maybe) {
    if (!maybe || maybe.length === 0) {
        return false;
    }
    return maybe[0].options !== undefined;
}
var ClearIndicator = function (props) { return (<react_select_1.components.ClearIndicator {...props}>
    <icons_1.IconClose size="10px"/>
  </react_select_1.components.ClearIndicator>); };
var DropdownIndicator = function (props) { return (<react_select_1.components.DropdownIndicator {...props}>
    <icons_1.IconChevron direction="down" size="14px"/>
  </react_select_1.components.DropdownIndicator>); };
var MultiValueRemove = function (props) { return (<react_select_1.components.MultiValueRemove {...props}>
    <icons_1.IconClose size="8px"/>
  </react_select_1.components.MultiValueRemove>); };
function SelectControl(props) {
    var theme = props.theme;
    // TODO(epurkhiser): The loading indicator should probably also be our loading
    // indicator.
    // Unfortunately we cannot use emotions `css` helper here, since react-select
    // *requires* object styles, which the css helper cannot produce.
    var indicatorStyles = function (_a) {
        var _padding = _a.padding, provided = tslib_1.__rest(_a, ["padding"]);
        return (tslib_1.__assign(tslib_1.__assign({}, provided), { padding: '4px', alignItems: 'center', cursor: 'pointer', color: theme.subText }));
    };
    var defaultStyles = {
        control: function (_, state) { return (tslib_1.__assign(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({ height: '100%', fontSize: theme.fontSizeLarge, lineHeight: theme.text.lineHeightBody, display: 'flex' }, {
            color: theme.formText,
            background: theme.background,
            border: "1px solid " + theme.border,
            boxShadow: "inset " + theme.dropShadowLight,
        }), { borderRadius: theme.borderRadius, transition: 'border 0.1s linear', alignItems: 'center', minHeight: '40px', '&:hover': {
                borderColor: theme.border,
            } }), (state.isFocused && {
            border: "1px solid " + theme.border,
            boxShadow: 'rgba(209, 202, 216, 0.5) 0 0 0 3px',
        })), (state.menuIsOpen && {
            borderBottomLeftRadius: '0',
            borderBottomRightRadius: '0',
            boxShadow: 'none',
        })), (state.isDisabled && {
            borderColor: theme.border,
            background: theme.backgroundSecondary,
            color: theme.disabled,
            cursor: 'not-allowed',
        })), (!state.isSearchable && {
            cursor: 'pointer',
        }))); },
        menu: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { zIndex: theme.zIndex.dropdown, marginTop: '-1px', background: theme.background, border: "1px solid " + theme.border, borderRadius: "0 0 " + theme.borderRadius + " " + theme.borderRadius, borderTop: "1px solid " + theme.border, boxShadow: theme.dropShadowLight })); },
        option: function (provided, state) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { lineHeight: '1.5', fontSize: theme.fontSizeMedium, cursor: 'pointer', color: state.isFocused
                ? theme.textColor
                : state.isSelected
                    ? theme.background
                    : theme.textColor, backgroundColor: state.isFocused
                ? theme.focus
                : state.isSelected
                    ? theme.active
                    : 'transparent', '&:active': {
                backgroundColor: theme.active,
            } })); },
        valueContainer: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { alignItems: 'center' })); },
        input: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { color: theme.formText })); },
        singleValue: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { color: theme.formText })); },
        placeholder: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { color: theme.formPlaceholder })); },
        multiValue: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { color: '#007eff', backgroundColor: '#ebf5ff', borderRadius: '2px', border: '1px solid #c2e0ff', display: 'flex' })); },
        multiValueLabel: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { color: '#007eff', padding: '0', paddingLeft: '6px', lineHeight: '1.8' })); },
        multiValueRemove: function () { return ({
            cursor: 'pointer',
            alignItems: 'center',
            borderLeft: '1px solid #c2e0ff',
            borderRadius: '0 2px 2px 0',
            display: 'flex',
            padding: '0 4px',
            marginLeft: '4px',
            '&:hover': {
                color: '#6284b9',
                background: '#cce5ff',
            },
        }); },
        indicatorsContainer: function () { return ({
            display: 'grid',
            gridAutoFlow: 'column',
            gridGap: '2px',
            marginRight: '6px',
        }); },
        clearIndicator: indicatorStyles,
        dropdownIndicator: indicatorStyles,
        loadingIndicator: indicatorStyles,
        groupHeading: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { lineHeight: '1.5', fontWeight: 600, backgroundColor: theme.backgroundSecondary, color: theme.textColor, marginBottom: 0, padding: space_1.default(1) + " " + space_1.default(1.5) })); },
        group: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { padding: 0 })); },
    };
    var getFieldLabelStyle = function (label) { return ({
        ':before': {
            content: "\"" + label + "\"",
            color: theme.gray300,
            fontWeight: 600,
        },
    }); };
    var async = props.async, creatable = props.creatable, options = props.options, choices = props.choices, clearable = props.clearable, components = props.components, styles = props.styles, value = props.value, inFieldLabel = props.inFieldLabel, rest = tslib_1.__rest(props, ["async", "creatable", "options", "choices", "clearable", "components", "styles", "value", "inFieldLabel"]);
    // Compatibility with old select2 API
    var choicesOrOptions = convertFromSelect2Choices_1.default(typeof choices === 'function' ? choices(props) : choices) ||
        options;
    // It's possible that `choicesOrOptions` does not exist (e.g. in the case of AsyncSelect)
    var mappedValue = value;
    if (choicesOrOptions) {
        /**
         * Value is expected to be object like the options list, we map it back from the options list.
         * Note that if the component doesn't have options or choices passed in
         * because the select component fetches the options finding the mappedValue will fail
         * and the component won't work
         */
        var flatOptions_1 = [];
        if (isGroupedOptions(choicesOrOptions)) {
            flatOptions_1 = choicesOrOptions.flatMap(function (option) { return option.options; });
        }
        else {
            // @ts-ignore The types used in react-select generics (OptionType) don't
            // line up well with our option type (SelectValue). We need to do more work
            // to get these types to align.
            flatOptions_1 = choicesOrOptions.flatMap(function (option) { return option; });
        }
        mappedValue =
            props.multiple && Array.isArray(value)
                ? value.map(function (val) { return flatOptions_1.find(function (option) { return option.value === val; }); })
                : flatOptions_1.find(function (opt) { return opt.value === value; }) || value;
    }
    // Override the default style with in-field labels if they are provided
    var inFieldLabelStyles = {
        singleValue: function (base) { return (tslib_1.__assign(tslib_1.__assign({}, base), getFieldLabelStyle(inFieldLabel))); },
        placeholder: function (base) { return (tslib_1.__assign(tslib_1.__assign({}, base), getFieldLabelStyle(inFieldLabel))); },
    };
    var labelOrDefaultStyles = inFieldLabel
        ? react_select_1.mergeStyles(defaultStyles, inFieldLabelStyles)
        : defaultStyles;
    // Allow the provided `styles` prop to override default styles using the same
    // function interface provided by react-styled. This ensures the `provided`
    // styles include our overridden default styles
    var mappedStyles = styles
        ? react_select_1.mergeStyles(labelOrDefaultStyles, styles)
        : labelOrDefaultStyles;
    var replacedComponents = {
        ClearIndicator: ClearIndicator,
        DropdownIndicator: DropdownIndicator,
        MultiValueRemove: MultiValueRemove,
        IndicatorSeparator: null,
    };
    return (<SelectPicker styles={mappedStyles} components={tslib_1.__assign(tslib_1.__assign({}, replacedComponents), components)} async={async} creatable={creatable} isClearable={clearable} backspaceRemovesValue={clearable} value={mappedValue} isMulti={props.multiple || props.multi} isDisabled={props.isDisabled || props.disabled} options={options || choicesOrOptions} openMenuOnFocus={props.openMenuOnFocus === undefined ? true : props.openMenuOnFocus} {...rest}/>);
}
var SelectControlWithTheme = react_1.withTheme(SelectControl);
function SelectPicker(_a) {
    var async = _a.async, creatable = _a.creatable, forwardedRef = _a.forwardedRef, props = tslib_1.__rest(_a, ["async", "creatable", "forwardedRef"]);
    // Pick the right component to use
    // Using any here as react-select types also use any
    var Component;
    if (async && creatable) {
        Component = async_creatable_1.default;
    }
    else if (async && !creatable) {
        Component = async_1.default;
    }
    else if (creatable) {
        Component = creatable_1.default;
    }
    else {
        Component = react_select_1.default;
    }
    return <Component ref={forwardedRef} {...props}/>;
}
// The generics need to be filled here as forwardRef can't expose generics.
var RefForwardedSelectControl = React.forwardRef(function RefForwardedSelectControl(props, ref) {
    return <SelectControlWithTheme forwardedRef={ref} {...props}/>;
});
exports.default = RefForwardedSelectControl;
//# sourceMappingURL=selectControl.jsx.map