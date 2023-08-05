Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var imageViewer_1 = tslib_1.__importDefault(require("app/components/events/attachmentViewers/imageViewer"));
var ImageVisualization = styled_1.default(imageViewer_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n  height: 100%;\n  img {\n    width: auto;\n    height: 100%;\n    object-fit: cover;\n    flex: 1;\n  }\n"], ["\n  padding: 0;\n  height: 100%;\n  img {\n    width: auto;\n    height: 100%;\n    object-fit: cover;\n    flex: 1;\n  }\n"])));
exports.default = ImageVisualization;
var templateObject_1;
//# sourceMappingURL=imageVisualization.jsx.map