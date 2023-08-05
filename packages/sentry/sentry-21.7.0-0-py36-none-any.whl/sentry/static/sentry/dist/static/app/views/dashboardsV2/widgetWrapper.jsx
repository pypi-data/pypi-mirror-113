Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var WidgetWrapper = styled_1.default(framer_motion_1.motion.div)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  touch-action: manipulation;\n\n  ", ";\n"], ["\n  position: relative;\n  touch-action: manipulation;\n\n  ", ";\n"])), function (p) {
    switch (p.displayType) {
        case 'big_number':
            return "\n          /* 2 cols */\n          grid-area: span 1 / span 2;\n\n          @media (min-width: " + p.theme.breakpoints[0] + ") {\n            /* 4 cols */\n            grid-area: span 1 / span 1;\n          }\n\n          @media (min-width: " + p.theme.breakpoints[3] + ") {\n            /* 6 and 8 cols */\n            grid-area: span 1 / span 2;\n          }\n        ";
        default:
            return "\n          /* 2, 4, 6 and 8 cols */\n          grid-area: span 2 / span 2;\n        ";
    }
});
exports.default = WidgetWrapper;
var templateObject_1;
//# sourceMappingURL=widgetWrapper.jsx.map